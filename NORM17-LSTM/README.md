# Normalisation of Modern French with an LSTM 'NMT' model

## Requirements

- Tested with Python>=3.7
- Install python dependencies: `pip install -r requirements.txt`
- Download model: `bash download_model.sh`

## Basic Usage

From untokenised text, input directly from standard input

```
>> echo "D'autres loin de ſe taire en ce meſme moment," | bash run_normalisation.sh

D'	D'
autres	autres
loin	loin
de	de
ſe	se
taire	taire
en	en
ce	ce
meſme	même
moment	moment
,	,

```

N.B. The tokenisation used (scripts found in align/) is from [pie-taggers, v0.0.13](https://github.com/hipster-philology/nlp-pie-taggers/blob/80a1b7477abb4abaaac943c793cf1fb2c106749a/pie_extended/models/fr/tokenizer.py). The necessary files for tokenised have been copied here (in `align/`) to avoid having to import heavy dependencies.


## Notes on the normalised text

There can be differences in segmentation between the original text and the normalised version that would be lost with the above token-level alignment. In the normalised version, where the left/right boundary of a word does not represent a word boundary, it is marked with an initial/final '▁'.

E.g. 'long tems' normalised to 'longtemps':

```
long  long▁
tems  ▁temps
```



## TEI format

TODO


