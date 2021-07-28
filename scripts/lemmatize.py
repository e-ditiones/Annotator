from lxml import etree
from pie_extended.cli.sub import get_tagger, get_model
# Change fr to freem for early modern french.
from pie_extended.models.fr.imports import get_iterator_and_processor
import os
import re
import csv
import argparse
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("file", help="file to process")
args = arg_parser.parse_args()

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}


# LEMMATIZATION ###############################################################

def lemmatize(doc):
    """
    This function process a lemmatization of the text.

    :param doc: a list of tags
    """
    # Change fr to freem for early modern french.
    model_name = "fr"
    tagger = get_tagger(model_name, batch_size=256, device="cpu", model_path=None)

    data = []

    segs = doc.xpath('//tei:seg', namespaces=ns)
    for seg in segs:
        iterator, processor = get_iterator_and_processor()
        # There are two lemmatizations, one with the text with 'ſ' (named orig_lemmas), the other with 's' (nammed lemmas)
        seg_s = seg.text.replace('ſ', 's')
        orig_lemmas = tagger.tag_str(seg.text, iterator=iterator, processor=processor)
        lemmas = tagger.tag_str(seg_s, iterator=iterator, processor=processor)

        # We check that both lists are still sames.        
        assert len(orig_lemmas) == len(lemmas)
        for index in range(len(lemmas)):
            output = {}
            output["token"] = orig_lemmas[index]['form']
            if lemmas[index]['lemma'] != None:
                output["lemma"] = lemmas[index]['lemma']
            if lemmas[index]['POS'] != None:
                output["pos"] = lemmas[index]['POS']
            if lemmas[index]['morph'] != None:
                msd = lemmas[index]['morph']
                output['msd'] = msd
                if 'MORPH' in msd:
                    morph = re.search(r'MORPH=.*', msd)
                    output['msd_morph'] = morph.group(0)
                if 'MODE' in msd:
                    output['msd_mode'] = re.search(r'MODE=[a-z]*\|', msd).group(0)
                if 'TEMS' in msd:
                    output['msd_tems'] = re.search(r'TEMS=.*\|', msd).group(0)
                if 'PERS' in msd:
                    output['msd_pers'] = re.search(r'PERS\.=.', msd).group(0)
                if 'NOMB' in msd:
                    output['msd_nomb'] = re.search(r'NOMB\.=.', msd).group(0)
                if 'GENRE' in msd:
                    output['msd_genre'] = re.search(r'GENRE=.', msd).group(0)
                if 'CAS' in msd:
                    output['msd_cas'] = re.search(r'CAS=.', msd).group(0)

            data.append(output)

    return data



if __name__ == "__main__":
    parser = etree.XMLParser(remove_blank_text=True)
    doc = etree.parse(args.file, parser)
    data = lemmatize(doc)

    with open('output/data.csv', 'w+', newline='') as csvfile:
        fieldnames = ['token', 'lemma', 'pos', 'msd', 'msd_morph', 'msd_mode', 'msd_temps', 'msd_pers', 'msd_nomb', 'msd_genre', 'msd_cas']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        for item in data:
            writer.writerow(item)
