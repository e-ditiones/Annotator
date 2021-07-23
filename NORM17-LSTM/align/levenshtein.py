#!/usr/bin/python
import numpy as np
import math
#from Levenshtein import distance
from utils import *
import os
import pickle

def get_correspondences(backpointers, len_ref, len_hyp):
    ref2hyp = {}
    i, j = len_hyp, len_ref
    while True:
        if j not in ref2hyp:
            ref2hyp[j] = []
        ref2hyp[j].append(i)
        if (i, j) == (1, 1):
            break
        previous = backpointers[(i, j)]
        i, j = previous # new indices                                                                                                                                                                                 
    return ref2hyp

def add_token_boundaries(hyp_idxs, hyp_word, orig_hyp):
    if len(hyp_idxs) == 0:
        return hyp_word
    prev_idx = min(hyp_idxs) - 1
    foll_idx = max(hyp_idxs) + 1
    if prev_idx == -1 or orig_hyp[prev_idx] == ' ':
        hyp_word = '▁' + hyp_word
    if foll_idx == len(orig_hyp) or orig_hyp[foll_idx] == ' ':
        hyp_word += '▁'

    return hyp_word

def int2str(orig_string, idxs):
    new_string = ''
    for idx in sorted(list(set(idxs))):
        if orig_string[idx] == ' ':
            new_string += '▁'
        else:
            if idx != '▁': # this could happen if a token boundary is added in before conversion to string
                new_string += orig_string[idx]
            else:
                new_string += idx
    return re.sub('▁+', '▁', new_string)

'''
Segment the hypothesis with respect to the tokenised reference
'''
def segment_hyp(ref, hyp, correspondences):
    aligned_words = []
    ref_word_idxs, hyp_word_idxs = [], []
    hyp_idxs_covered = [] # list of hyp indices covered

    # go through reference                                                                                                                                                         
    for i in range(0, len(ref)):
        # matching idxs with hypothesis (in correct rather than reverse order). Also start from 0
        match_hyp_idxs = [x - 1 for x in correspondences[i + 1][::-1]]
        #print(i, 'ref = "' + ref[i]+'"', match_hyp_idxs, [hyp[x] for x in match_hyp_idxs])
        # if finished a ref word (i.e. whitespace), store the current matching ref and hyp words and start a new one
        if ref[i] == ' ':
            hyp_word_idxs.extend([j for j in match_hyp_idxs if hyp[j] != ' '])
            new_hyp_word_idxs = list(set([j for j in hyp_word_idxs if j not in hyp_idxs_covered]))
            hyp_idxs_covered.extend(new_hyp_word_idxs) # avoid repetition of hypothesis indices
            aligned_words.append( ('▁' + int2str(ref, ref_word_idxs) + '▁', add_token_boundaries(new_hyp_word_idxs, int2str(hyp, new_hyp_word_idxs), hyp)) )
            #print(('▁' + int2str(ref, ref_word_idxs) + '▁', add_token_boundaries(new_hyp_word_idxs, int2str(hyp, new_hyp_word_idxs), hyp)))
            ref_word_idxs, hyp_word_idxs = [], []
            # add anything matched with the space
            hyp_idxs_covered.extend([j for j in match_hyp_idxs if j not in hyp_idxs_covered]) # avoid repetition of hypothesis indices
        else:
            ref_word_idxs.append(i)
            hyp_word_idxs.extend(match_hyp_idxs)

    # add final words
    new_hyp_word_idxs = list(set([i for i in hyp_word_idxs if i not in hyp_idxs_covered]))
    hyp_idxs_covered.extend(new_hyp_word_idxs)
    aligned_words.append( ('▁' + int2str(ref, ref_word_idxs) + '▁', add_token_boundaries(hyp_word_idxs, int2str(hyp, new_hyp_word_idxs), hyp)) )

    # check that all idxs are present (only once)
    assert all([hyp_idxs_covered.count(i) == 1 for i in range(len(hyp)) if hyp[i] != ' ']), 'All hypotheses indices but must covered by alignment'

    return aligned_words

def levenshtein(ref, hyp):
    len_hyp = len(hyp) + 1
    len_ref = len(ref) + 1
    # initialise matrix
    matrix = np.zeros((len_hyp, len_ref))
    backpointers = {}
    for i in range(len_hyp):
        matrix[i, 0] = i
    for i in range(len_ref):
        matrix[0, i] = i

    for i in range(1, len_hyp):
        for j in range(1, len_ref):
            deletion = matrix[i-1, j] + 1
            insertion = matrix[i, j-1] + 1
            substitution = matrix[i-1, j-1]
            if hyp[i-1] != ref[j-1]:
                substitution += 1
            matrix[i, j] = min(deletion, insertion, substitution)
            # get backpointers
            if (i, j) != (1, 1):
                if deletion == matrix[i, j]:
                    backpointers[(i, j)] = (i-1, j)
                elif insertion == matrix[i, j]:
                    backpointers[(i, j)] = (i, j-1)
                else:
                    backpointers[(i, j)] = (i-1, j-1)

    return (matrix[len_hyp - 1, len_ref - 1]), matrix, backpointers


def calculate_score(ref_file, hyp_file, type_seg, cache_file=None):
    dist, dist2 = 0, 0
    num_chars = 0

    # load cache scores
    cache_scores = {}
    if cache_file is not None and os.path.exists(cache_file):
        cache_scores = pickle.load(open(cache_file, 'rb'))
    
    with open(hyp_file) as hfp, open(ref_file) as rfp:
        for i, (h, r) in enumerate(zip(hfp, rfp)):
            # sometimes there are newlines at the end of the reference files so skip these
            # there should not be any blank lines elsewhere in the file
            if r.strip() == '':
                continue
            h, r = re.sub(' +', ' ', h).strip(), re.sub(' +', ' ', r).strip()
            if type_seg == 'char':
                if  ('@ ' + r, '@ ' + h) in cache_scores:
                    dist_tmp, aligned_words = cache_scores[('@ ' + r, '@ ' + h)]
                else:
                    # call levenshtein to get matrix and overall score (args: ref, then hyp)
                    dist_tmp, matrix, backpointers = levenshtein('@ ' + r, '@ ' + h)
                    # get the character-level alignment beteen the ref and the hyp
                    r2h = get_correspondences(backpointers, len(r) + 2, len(h) + 2)
                    # get the token-level alignment between the ref and the hyp
                    aligned_words = segment_hyp('@ ' + r, '@ ' + h, r2h)
                    # cache the scores
                    cache_scores[('@ ' + r, '@ ' + h)] = (dist_tmp, aligned_words)
            else:
                h, r = tokenise(h).split(), tokenise(r).split()
                if (tuple(['@'] + r), tuple(['@'] + h)) in cache_scores:
                    dist_tmp, aligned_words = cache_scores[(tuple(['@'] + r), tuple(['@'] + h))]
                else:
                    # call levenshtein to get matrix and overall score (args: ref, then hyp, but reversed here) 
                    dist_tmp, _, backpointers = levenshtein(['@'] + r, ['@'] + h)
                    r2h = get_correspondences(backpointers, len(r) + 1, len(h) + 1)
                    #print(r)
                    #print(h)
                    #print(r2h)
                    #for reftok in list(sorted(r2h.keys()))[1:]:
                    #    print((['@'] + r)[reftok - 1], end=': ')
                    #    print(r2h[reftok])
                    #    for x in r2h[reftok]:
                    #        print((['@'] + h)[x - 1], end=' ')
                    #    print()
                    aligned_words = [((['@'] + r)[reftok - 1], ' '.join([(['@'] + h)[x - 1] for x in r2h[reftok]])) for reftok in list(sorted(r2h.keys()))[1:]]
                    cache_scores[(tuple(['@'] + r), tuple(['@'] + h))] = (dist_tmp, aligned_words)
            dist += float(dist_tmp)/len(r)
            num_chars += len(r)

    # dump cache scores
    if cache_file is not None:
        pickle.dump(cache_scores, open(cache_file, 'wb'))
    
    print(round(math.log(dist/num_chars), 3))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('hyp')
    parser.add_argument('ref')
    parser.add_argument('--type_seg', choices=['char', 'tok'], required=True)
    parser.add_argument('--cache', default=None)
    args = parser.parse_args()
    
    calculate_score(args.ref, args.hyp, args.type_seg, args.cache)
