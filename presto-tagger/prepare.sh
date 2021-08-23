#!/bin/bash

# Create the directories for the model, data and the embeddings
mkdir logs
mkdir embeddings
mkdir data

# Download the embeddings, the model and the data 
wget https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.fr.300.bin.gz -P embeddings/
gunzip embeddings/cc.fr.300.bin.gz
curl https://sharedocs.huma-num.fr/wl/?id=Kq2woXBVoUv8BIyEQrIP0L0dv6XysWO3&fmode=download --output logs/prestov5.3-tagger.zip
unzip logs/prestov5.3-tagger.zip -d logs/
curl https://sharedocs.huma-num.fr/wl/?id=hNkFbpu7qU4uQsvRaPWM3mm8SEK5CypU&fmode=download --output data.zip
unzip data.zip -d data/
