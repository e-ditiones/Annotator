from lxml import etree
import csv
import os
import re
import glob

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

def update_xml(file):
    """
    This script is used to update some elements of the XML file to modify.
    """
    # Add a new type on the existing text element
    text_trans = doc.xpath('//tei:text[1]', namespaces=ns)[0]
    text_trans.attrib["type"] = "transcription"
    # Add a new text element (with annotation) and its children (body and p)
    text_annotation = etree.Element("{http://www.tei-c.org/ns/1.0}text")
    text_annotation.attrib["type"] = "annotation"
    text_trans.addnext(text_annotation)
    body = etree.SubElement(text_annotation, 'body')
    etree.SubElement(body,'p')


def get_annotations(tsv):
    """
    This script is used to get a list of annotated w elements.
    """

    annotated_file = csv.DictReader(tsv, delimiter='\t')
    list_w = []
    n = 1
    for row in annotated_file:
        if row['pos']=="PONfrt":
            ponc = etree.Element("{http://www.tei-c.org/ns/1.0}pc")
            ponc.text = row['token']
            list_w.append(ponc)
        else:
            word = etree.Element("{http://www.tei-c.org/ns/1.0}w")
            word.attrib["{http://www.w3.org/XML/1998/namespace}id"] = "w" + str(n)
            word.text = row['token']
            word.attrib['lemma'] = row['lemma']
            word.attrib['pos'] = row['pos']
            word.attrib['msd'] = row['msd']
            # Lorsque la normalisation fonctionnera, ajouter le résultat dans un attribut reg (solution retenue pour éviter de générer des fichiers trop lourds)
            #word.attrib['reg'] = row['norm']
            # NER : pareil que normalisation, solution temporaire.
            #word.attrib['type'] = row['ner']
            list_w.append(word)
            n += 1
        
    return list_w


    #return doc.write('output.xml',pretty_print=True, encoding="utf-8", method="xml")



if __name__ == "__main__":

    parser = etree.XMLParser(remove_blank_text=True)
    
    files = glob.glob("in_XML/**/*.xml", recursive=True)

    for file in files:
        id = os.path.basename(file)
        id = re.sub(".xml","",id)
        doc = etree.parse(file, parser)
        update_xml(doc)
        
        with open('out/TSV/%s.tsv' %(id), 'r', newline='') as tsvfile:
            result = get_annotations(tsvfile)
            p_annot = doc.xpath('//tei:text[@type="annotation"]/body/p', namespaces=ns)[0]
            p_annot.extend(result)

        doc.write('out/XML/%s-annotated.xml' %(id),pretty_print=True, encoding="utf-8", method="xml")