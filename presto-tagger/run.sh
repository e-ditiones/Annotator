./tagger.py --predict=logs/prestov5.3-tagger \
        --test_data=data_norm.csv \
        --fasttext_model=embeddings/cc.fr.300.bin \
        --name=LSTM-CRF-TEST \
        > resultat.csv
