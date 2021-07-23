#!/usr/bin/python
from levenshtein import *
import re, os
from utils import *

def align(src_file, hyp_file, cache_file, already_tokenised=False):
    # load cache_filescores
    cache_scores = {}
    if cache_file is not None and os.path.exists(cache_file):
        cache_scores = pickle.load(open(cache_file, 'rb'))

    with open(hyp_file, encoding='utf-8') as hfp, open(src_file, encoding='utf-8') as sfp:
        for hyp, src in zip(hfp, sfp):
            # get rid of any double spaces
            hyp, src = re.sub(' +', ' ', hyp), re.sub(' +', ' ', src)
            
            # tokenise in order to align on src whitespace later
            if not already_tokenised:
                hyp, src = tokenise(hyp.strip()), tokenise(src.strip())
            len_hyp, len_src = len(hyp), len(src)

            # get cached scores and alignments if they are there
            if ('@ ' + src, '@ ' + hyp) in cache_scores:
                dist, aligned_words = cache_scores[('@ ' + src, '@ ' + hyp)]
            else:
                dist, matrix, backpointers  = levenshtein('@ ' + src, '@ ' + hyp)
                s2h = get_correspondences(backpointers, len_src + 2, len_hyp + 2)
                aligned_words = segment_hyp('@ ' +src, '@ ' + hyp, s2h)
                cache_scores['@ ' + src, '@ ' + hyp] = (dist, aligned_words)

            # store in cache for later
            cache_scores['@ ' + src, '@ ' + hyp] = (dist, aligned_words)

            # print out alignment
            for a in aligned_words:
                if a[0] == '▁@▁':
                    continue
                src = postprocess_word(a[0])
                trg = postprocess_word(a[1])
                print('\t'.join([src, trg]))
                print(trg)
            print()
                
    # dump cache_filescores
    if cache_file is not None:
        pickle.dump(cache_scores, open(cache_file, 'wb'))
    

def postprocess_word(word):
    new_word = word
    if word[0] == '▁':
        new_word = new_word[1:]
    else:
        new_word = '▁' + new_word
    if word[-1] == '▁':
        new_word = new_word[:-1]
    else:
        new_word += '▁'
    return new_word

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('src', help='The source document to be aligned against (or srcerence if appropriate)')
    parser.add_argument('hyp', help='The hypothesis document to align against src')
    parser.add_argument('--cache', default=None)
    parser.add_argument('--already_tokenised', default=False, action='store_true')
    args = parser.parse_args()

    align(args.src, args.hyp, args.cache, args.already_tokenised)
