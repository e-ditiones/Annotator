from lxml import etree
import os
import csv
import pandas as pd
import subprocess
import argparse
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("file", help="file to process")
args = arg_parser.parse_args()

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

def normalize(doc):
    """
    This function process a normalization of the text.
    :param doc: an XML file
    :return: list containing the normalisation
    """
    token_norm = []
    segs = doc.xpath('//tei:seg', namespaces=ns)
    for seg in segs:
        token_norm_seg = []
        id = seg.xpath('./@xml:id', namespaces=ns)
        texte = seg.text.strip('\n')
        nb_token_source = len(texte.split())
        # Idéalement, on récupère la liste des tokens normalisés, voir le script NORM17-LSTMT/align/align.py pour la sortie
        token_norm_seg = subprocess.run(["NORM17-LSTM/run_normalisation.sh", texte])
        #assert nb_token_source == len(), 'Attention, le nombre de token de la source et le nombre de tokens normalisés ne sont pas les mêmes, voir segment' + id
        token_norm.append(token_norm_seg)

    # Attention, de mémoire les &amp; posent pb, les remplacer avant de les envoyer au script de Rachel
    return token_norm




if __name__ == "__main__":
    parser = etree.XMLParser(remove_blank_text=True)
    doc = etree.parse(args.file, parser)
    # on récupère une liste contenant l'ensemble des tokens normalisés et on l'ajoute au csv
    data_norm = normalize(doc)

    # AJOUT D'UNE COLONNE CONTENANT LA NORMALISATION
    #df = pd.read_csv("output/data.csv", delimiter='\t')
    #df["NORM_LSTM"] = "data_norm"
    #df.to_csv("output/data.csv", index=False)
