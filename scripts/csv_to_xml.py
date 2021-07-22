from lxml import etree
import csv
import argparse
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("csv", help="CSV file to process")
arg_parser.add_argument("xml", help="XML file to process")
args = arg_parser.parse_args()

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

# Se servir du script level2to3.py qui permet déjà de consituer l'encodage de niveau 3.
# Prendre le fichier xml _3 en entrée (on conserve ainsi les segments) et en modifier le contenu

if __name__ == "__main__":
    parser = etree.XMLParser(remove_blank_text=True)
    doc = etree.parse(args.file, parser)


    doc.write(args.file, pretty_print=True, encoding="utf-8", method="xml")