# Annotator

This script process segmentation, lemmatization, normalization and NER of XML-TEI encoded files. 

## Getting starded

## TO DO

Normalization and NER are still a work in progress.

### To install Annotator, using command lines, you have to :

* clone or download this repository
```bash
git clone https://github.com/e-ditiones/Annotator.git
cd Annotator
```

### How to use it

1. The XML-files to be processed need to be in the `in_XML` folder.

2. Run the script
```bash
bash process.sh
```

3. Results are in the `out` folder :
	- `XML` : contains XML annotated files ;
	- `TSV` : contains the annotation in TSV format.

## How it works


### The lemmazition

For lemmatisation, we use [_Pie-extended_](https://github.com/hipster-philology/nlp-pie-taggers) and the "[freem](https://github.com/hipster-philology/nlp-pie-taggers/tree/master/pie_extended/models/freem)" model.


## Credits 

This repository is developed by Alexandre Bartz with the help of Simon Gabay, as part of the project [e-ditiones](https://github.com/e-ditiones).


## Licences

<a rel="licence" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Licence Creative Commons" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />Our work is licenced under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International Licence</a>.

[_Pie-extended_](https://github.com/hipster-philology/nlp-pie-taggers) is under the [Mozilla Public License 2.0](https://www.mozilla.org/en-US/MPL/2.0/).


## Cite this repository À CHANGER

Alexandre Bartz, Simon Gabay. 2020. _Lemmatization and normalization of French modern manuscripts and printed documents_. Retrieved from https://github.com/e-ditiones/Annotator.
