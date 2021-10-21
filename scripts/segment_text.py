from lxml import etree
import json
import os
import re
import argparse
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("file", help="file to process")
args = arg_parser.parse_args()

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

# SEGMENTATION ################################################################


def transform_text(doc):
    """
    This function removes unsupported tags from a given doc.

    :param doc: XML document
    :return: XML doc after transformation
    :rtype: XLM doc
    """
    xslt = etree.parse('scripts/XSLT/clean_text.xsl')
    transform = etree.XSLT(xslt)
    doc_transf = transform(doc)
    return doc_transf


def segment_text(text):
    """
    This function is used to segment the text and wrap these segments with <seg> elements.

    :param doc: text
    :return: a list of segments
    :rtype: list
    """
    segments = re.findall(r"[^\.\?:\;!]+[\.\?:\;!]?", text)
    list = []
    n = 1
    for segment in segments:
        # This makes sure no <seg> is empty
        text = segment.strip()
        if text:
            seg = etree.Element("{http://www.tei-c.org/ns/1.0}seg")
            seg.text = text
            seg.attrib["n"] = str(n)
            # The xml:id attribute is generated with the value of the n attribute.
            seg.attrib["{http://www.w3.org/XML/1998/namespace}id"] = "s" + seg.get("n")
            n += 1
            list.append(seg)
    return list


def segment_elements(list_elements):
    """
    For each element, this function adds the text in the new <seg> elements.

    :param doc: a list of XML elements
    """
    for element in list_elements:
        text = element.text
        segs = segment_text(text)
        # This removes the text before we add it in the new <seg> element.
        element.clear()
        element.extend(segs)


def segment(doc):
    """
    For each lines and paragraphs, this function segments the text.

    :param doc: a XML document
    :return: a level 3 XML document
    :rtype: a new XLM document
    """
    # Only the text enclosed between <p> and <l> is segmented.
    paragraphs = doc.xpath('//tei:text//tei:p', namespaces=ns)
    lines = doc.xpath('//tei:text//tei:l', namespaces=ns)
    segment_elements(paragraphs)
    segment_elements(lines)
    # This output file is specific to the project e-ditiones, you can easily change the output with e.g. doc.write("New" + args.file, ...)
    return doc.write(args.file.replace(".xml", "_segmented.xml"), pretty_print=True, encoding="utf-8", method="xml")


def rebuild_words(doc):
    """
    Used to rebuild a word separated by a lb element.
    For example :
    <lb/>I hope this script is use
    <lb break='no' rend='-'/>ful
    will give :
    <lb/>I hope this script is useful
    --> then all words can be tokenized correctly.

    :param doc: a XML document
    :return: the same document with rebuilt word.
    :rtype: a new XLM document
    """
    # For each line break wich splits a word in two, we want to remove it and reform the word.
    for lb in doc.xpath("//tei:lb[@break='no']", namespaces=ns):
        # We get the text where the first part of the word belongs.
        previous = lb.getprevious()
        # We get the second part.
        tail = lb.tail if lb.tail is not None else ""
        # We want to be sure that the element contains a string and we want to be sure that there is some text.
        # This prevents encoding errors.
        if previous != None and previous.tail != None:
            previous.tail = previous.tail.rstrip() + tail
        # Otherwise, we get the text of the parent element and we want to be sure that there is some text.
        elif lb.getparent().tail != None :
            lb.getparent().text = lb.getparent().text.rstrip() + tail
        lb.getparent().remove(lb)


if __name__ == "__main__":
    parser = etree.XMLParser(remove_blank_text=True)
    doc = etree.parse(args.file, parser)
    rebuild_words(doc)
    text_transformed = transform_text(doc)
    segment(text_transformed)
