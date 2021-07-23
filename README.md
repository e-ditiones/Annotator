# SEG17

This script process segmentation, normalization and lemmatization of XML-TEI encoded files. 

## Getting starded

#### To install SEG17, using command lines, you have to :

* clone or download this repository
```bash
git clone git@github.com:e-ditiones/SEG17.git
cd SEG17
```

#### Segmentation

1. create a first virtual environment and activate it
```bash
python3 -m venv env
source env/bin/activate
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

1. The virtual env to be used is `env`.

2. install lemmatisation models
```
PIE_EXTENDED_DOWNLOADS=~/MesModelsPieExtended pie-extended download fr
```
3. if you want to **lemmatize** your segmented file
```bash
PIE_EXTENDED_DOWNLOADS=~/MesModelsPieExtended python3 scripts/lemmatize path/to/file_segmented.xml
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
2. install dependencies
```bash
pip install -r NORM17-LSTM/requirements.txt
```
3. download the model
```bash
cd NORM17-LSTM
bash download_model.sh
```
4. if you want to **normalize** your segmented file
```bash
cd ..
python3 scripts/normalize_lstm.py path/to/file_segmented
```
5. The file `output/data.csv` will be updated and contain the result of the normalisation.

#### NER

#### Get an XML file

Using the created csv file, `csv_to_xml.py` will constitute an XML file.

1. First, you have to deactivate the previous virtual env, using 
```bash
deactivate
```
2. Then, activate the first virutal env
```bash
source env/bin/activate
```
3. Get the annotated XML file
```bash
python3 scripts/csv_to_xml.py path/to/file_segmented
```
4. You will get `file_annotated.xml`.


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
