from lxml import etree
import csv
import argparse
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("csv", help="CSV file to process")
arg_parser.add_argument("xml", help="XML file to process")
args = arg_parser.parse_args()

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

# Se servir du script level2to3.py qui permet déjà de consituer l'encodage de niveau 3.

# L'idée de se script est de reconstituer un fichier XML à partir du csv
# Pour reconstituer les segments, utiliser la ponctuation forte (dans le csv, colonne POS)


def get_xml_file(csv_file):
    """
    This script is used to reconstruct an XML-TEI file using a CSV.
    :param csv_file: a csv_file
    :param xml_file: an xml_file
    :return: an XML file
    """


    return doc.write('output.xml',pretty_print=True, encoding="utf-8", method="xml")



if __name__ == "__main__":

    with open('output/corpus.csv', 'w+', newline='') as csvfile:
        get_xml_file(csvfile)

    doc.write('output.xml',pretty_print=True, encoding="utf-8", method="xml")