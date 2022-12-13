#!/bin/bash

# Bash script used to annotate XML-TEI files : lemmatization, normalization and NER.

# The bash code used to generate/activate virtual environnements has been inspired from 
# https://github.com/Gallicorpora/application, scripts written by Kelly Christensen.

# The normalization and NER are still a work in progress. 

# ---------------------------------------------------------------------------------

# Input : XML-TEI files
# Output :
#	- XML-TEI annotated files
#	- TSV files 

# There are 5 steps :
# 1. Segmentation
# 2. Lemmatization (lemma, pos, msd)
# 3. Normalization
# 4. NER
# 5. Build XML-TEI annotated files


#######################################################################################

# SEGMENTATION

ENV=segmentation
FILE=seg_requirements.txt

python3.9 -m venv ".venvs/${ENV}"
source ".venvs/${ENV}/bin/activate"
pip install --upgrade pip
pip install -r "requirements/${FILE}"

python scripts/segment_text.py

deactivate

# ---------------------------------------------------------------------------------

# LEMMATIZATION

ENV=lemmatization
FILE=lemmatization_requirements.txt

python3.7 -m venv ".venvs/${ENV}"
source ".venvs/${ENV}/bin/activate"
pip install --upgrade pip
pip install -r "requirements/${FILE}"

# Install lemmatization models

#PIE_EXTENDED_DOWNLOADS=~/MesModelsPieExtended pie-extended download freem

# Run script

PIE_EXTENDED_DOWNLOADS=~/MesModelsPieExtended python3.7 scripts/lemmatize.py

deactivate

# ---------------------------------------------------------------------------------

#### TO DO ####

# NORMALIZATION
#
#ENV=normalization
#FILE=normalization_requirements.txt
#
#python3.7 -m venv ".venvs/${ENV}"
#source ".venvs/${ENV}/bin/activate"
#pip install --upgrade pip
#pip install -r "requirements/${FILE}"
#
## Download model
#
##bash models/NORM17-LSTM/download_model.sh
#
## Run script
#
#cd models/NORM17-LSTM
#
#python3.7 ../../scripts/normalize_lstm.py
#
rm in_XML/*_segmented.xml
#
#deactivate

# ---------------------------------------------------------------------------------

#### TO DO ####

# NER

#ENV=ner
#FILE=ner_requirements.txt
#
#python3.7 -m venv ".venvs/${ENV}"
#source ".venvs/${ENV}/bin/activate"
#pip install --upgrade pip
#pip install -r "requirements/${FILE}"

#
##bash models/presto-tagger/prepare.sh
#
#cd models/presto-tagger
#python3.7 ../../scripts/ner.py
#
#deactivate

# ---------------------------------------------------------------------------------

# GET XML

# We can reuse the segmentation venv
ENV=segmentation

python3.9 -m venv ".venvs/${ENV}"

python3.9 scripts/to_xml.py

deactivate


