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

    texte_list = doc.xpath('//tei:seg/text()', namespaces=ns)
    texte_str = "\n".join(texte_list)
    # remplacement des tirets car ils empêchent le fonctionnement du normalisateur (à corriger plus tard)
    texte_str_propre = texte_str.replace("-", " ")
    # Idéalement, on récupère la liste des tokens normalisés, voir le script NORM17-LSTMT/align/align.py pour la sortie
    token_norm = subprocess.check_output(["bash", "run_normalisation_param.sh", texte_str_propre])
    token_norm_decode = token_norm.decode("utf-8")
    token_norm_list = token_norm_decode.split("\n")
    list_norm = []
    for el in token_norm_list:
        if '\t' in el:
            el_propre = el.split('\t')
            list_norm.append(el_propre)
        else:
            pass
    print(list_norm)
    # assert nb_token_source == len(), 'Attention, le nombre de token de la source et le nombre de tokens normalisés ne sont pas les mêmes, voir segment' + id
    # Attention, de mémoire les &amp; posent pb, les remplacer avant de les envoyer au script de Rachel
    return list_norm


if __name__ == "__main__":
    parser = etree.XMLParser(remove_blank_text=True)
    doc = etree.parse(args.file, parser)
    # on récupère une liste contenant l'ensemble des tokens normalisés et on l'ajoute au csv
    list_norm = normalize(doc)

    # AJOUT D'UNE COLONNE CONTENANT LA NORMALISATION
    df = pd.read_csv("../output/data.csv", delimiter=',')
    df['norm']=""
    for n in range(0, len(df)):
        token = df.loc[n].token
        for el in list_norm:
            if el[0] == token:
                df.at[n, 'norm'] = el[1]
    df.to_csv("../output/data.csv", index=False)

