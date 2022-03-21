# Annotator

This script process segmentation, lemmatization, normalization and NER of XML-TEI encoded files. 

## Getting starded

#### To install SEG17, using command lines, you have to :

* clone or download this repository
```bash
git clone https://github.com/e-ditiones/Annotator.git
cd Annotator
```

#### Segmentation

1. create a first virtual environment and activate it
```bash
python3 -m venv seg
source seg/bin/activate
```
2. install dependencies
```bash
pip install -r requirements.txt
```
3. if you want to **split** your text
```bash
python3 scripts/segment_text.py path/to/file
```
4. You will get `filename_segmented.xml`.


#### Lemmatisation

1. The virtual env to be used is `seg`.

2. install lemmatisation models
```
PIE_EXTENDED_DOWNLOADS=~/MesModelsPieExtended pie-extended download fr
```
3. if you want to **lemmatize** your segmented file
```bash
PIE_EXTENDED_DOWNLOADS=~/MesModelsPieExtended python3 scripts/lemmatize.py path/to/file_segmented.xml
```
4. In `output/data.csv`, you will find the results of the lemmatisation.


#### Normalisation LSTM

1. First, you have to deactivate the previous virtual env, using :
```bash
deactivate
```
2. create a second virtual environment and activate it
```bash
python3 -m venv norm_lstm
source norm_lstm/bin/activate
```
3. install dependencies
```bash
pip install -r NORM17-LSTM/requirements.txt
```
4. download the model
```bash
cd NORM17-LSTM
bash download_model.sh
```
5. if you want to **normalize** your segmented file
```bash
python3 ../scripts/normalize_lstm.py ../path/to/file_segmented
```
6. The file `output/data.csv` will be updated and contain the result of the normalisation.

#### NER

1. First, you have to deactivate the previous virtual env, using 
```bash
deactivate
```
2. Then, create a new first virutal env
```bash
cd ..
python3 -m venv ner
source ner/bin/activate
```
3. install dependencies
```bash
pip install -r NORM17-LSTM/requirements.txt
```
4. install model
```
cd presto-tagger
bash prepare.sh
```

Download https://sharedocs.huma-num.fr/wl/?id=hNkFbpu7qU4uQsvRaPWM3mm8SEK5CypU&fmode=download, uncompress it and replace the existing `data` folder with it.

Download https://sharedocs.huma-num.fr/wl/?id=Kq2woXBVoUv8BIyEQrIP0L0dv6XysWO3&fmode=download and uncompress it in the logs folder.

5. if you want to do ***NER*** on your file:
```
python3 ../scripts/ner.py ../output/data.csv
```

6. The file `output/data.csv` will be updated and contain the result of the ner.

#### NER with Wikidata

1. First, you have to deactivate the previous virtual env, using 
```bash
deactivate
```
2. Then, create a new first virutal env
```bash
cd ..
python3 -m venv wiki
source wiki/bin/activate
```
3. install dependencies
```bash
pip install -r wikidataMultisearch/requirements.txt
```
4. run the script (!à modifier, passer des Args)
```bash
python3 wikidataMultisearch/wikidataMultisearch.py
```
5. The updated file will be in `output` and be named `data.csv.wikidata.tsv`

#### Get an XML file

1. Be sure that `????` is activated.


2. Get the annotated XML file
Using the created csv file, `csv_to_xml.py` will constitute an XML file.
```bash
python3 scripts/csv_to_xml.py XML/path/to/file_segmented
```
3. You will get `file_annotated.xml` in the folder `XML`.


## How it works

### The segmentation

Using the `Level-2_to_level-3.xsl` XSL stylesheet, the script adds XML-TEI tags to split the text in segments (`<seg>`).
For each `<p>`(paragraph) and `<l>`(line), using some poncuation marks (.;:!?), the script `level2to3.py` split the text in segments captured in `<seg>` elements.


### The lemmazition

For lemmatisation, we use [_Pie-extended_](https://github.com/hipster-philology/nlp-pie-taggers) and the "[fr](https://github.com/hipster-philology/nlp-pie-taggers/tree/f3dd5197cd0a70381e008ab8239d47aff04c9737/pie_extended/models/fr)" model.

The original version, and not the normalised version, is lemmatised.


## Credits À CHANGER

This repository is developed by Alexandre Bartz with the help of Simon Gabay, as part of the project [e-ditiones](https://github.com/e-ditiones).


## Licences

<a rel="licence" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Licence Creative Commons" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />Our work is licenced under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International Licence</a>.

[_Pie-extended_](https://github.com/hipster-philology/nlp-pie-taggers) is under the [Mozilla Public License 2.0](https://www.mozilla.org/en-US/MPL/2.0/).

[_Morphalou_](https://www.ortolang.fr/market/lexicons/morphalou) is under the [LGPL-LR](https://spdx.org/licenses/LGPLLR.html).

## Cite this repository À CHANGER

Alexandre Bartz, Simon Gabay. 2020. _Lemmatization and normalization of French modern manuscripts and printed documents_. Retrieved from https://github.com/e-ditiones/SEG17.
