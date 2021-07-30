./tagger.py --predict=logs/prestov5.3-tagger \
        --test_data=data/test-data.conll \
        --fasttext_model=embeddings/cc.fr.300.bin \
        --name=LSTM-CRF-TEST \
        > data/result_test_data.conll