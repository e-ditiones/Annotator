# Normalisation of Modern French with an LSTM 'NMT' model

## Requirements

- Tested with Python==3.7
- Install python dependencies: `pip install -r requirements.txt`
- prepare model: `bash prepare.sh`

## Basic Usage

From conll format file with underscores at the 4th column (see `data/test_data`), modify the `run.sh` script where the second line points to the file you want to tag and the fifth line points to the destination file.

```
>> bash run.sh
```

## TEI format

TODO


Source code: Neural Architectures for Nested NER through Linearization
======================================================================
Jana Straková, Milan Straka and Jan Hajič
https://aclweb.org/anthology/papers/P/P19/P19-1527/
{strakova,straka,hajic}@ufal.mff.cuni.cz

License
-------

Copyright 2019 Institute of Formal and Applied Linguistics, Faculty of
Mathematics and Physics, Charles University, Czech Republic.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.

Please cite as:
---------------

```
@inproceedings{strakova-etal-2019-neural,
    title = "Neural Architectures for Nested {NER} through Linearization",
    author = "Strakov{\'a}, Jana  and
      Straka, Milan  and
      Hajic, Jan",
    booktitle = "Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2019",
    address = "Florence, Italy",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/P19-1527",
    doi = "10.18653/v1/P19-1527",
    pages = "5326--5331",
    abstract = "We propose two neural network architectures for nested named entity recognition (NER), a setting in which named entities may overlap and also be labeled with more than one label. We encode the nested labels using a linearized scheme. In our first proposed approach, the nested labels are modeled as multilabels corresponding to the Cartesian product of the nested labels in a standard LSTM-CRF architecture. In the second one, the nested NER is viewed as a sequence-to-sequence problem, in which the input sequence consists of the tokens and output sequence of the labels, using hard attention on the word whose label is being predicted. The proposed methods outperform the nested NER state of the art on four corpora: ACE-2004, ACE-2005, GENIA and Czech CNEC. We also enrich our architectures with the recently published contextual embeddings: ELMo, BERT and Flair, reaching further improvements for the four nested entity corpora. In addition, we report flat NER state-of-the-art results for CoNLL-2002 Dutch and Spanish and for CoNLL-2003 English.",
}
```
