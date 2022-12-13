import pandas as pd
import subprocess
import glob
import os
import re

def ner(dataframe, id):
    """
    This function process a ner of the text.
    :param dataframe: dataframe
    :return: list containing the ner
    """
    # je récupère la colonne norm sous forme d'un dataframe a une seule colonne
    list_col_norm = dataframe['token'].copy()
    # je la mets dans un csv avec une seule colonne
    df = pd.DataFrame(list_col_norm)
    df.to_csv('data_norm.csv', sep="\t", encoding="utf8", escapechar="\n", index=False)
    # lancement de la commande
    subprocess.run(["bash", "run.sh"])

    # je récupère l'output et la colonne ner '
    df_ner = pd.read_csv('resultat.csv', delimiter='\t')
    print(df_ner)
    df_ner.set_axis(['norm', '0', '0', 'ner'],axis='columns', inplace=True)
    dict_ner = dict(zip(df_ner.norm, df_ner.ner))
    return dict_ner

if __name__ == "__main__":
    files = glob.glob("../../out/TSV/*.tsv")

    for file in files:
        id = os.path.basename(file)
        id = re.sub(".xml","",id)
        df = pd.read_csv(file, delimiter='\t')
        # lancement de la fonction
        dict_ner = ner(df, id)
        df['ner'] = ""
        for n in range(0, len(df)):
            token = df.loc[n].norm
            for el in dict_ner:
                if el == token:
                    df.at[n, 'ner'] = dict_ner[token]

        # écriture dans le csv
        df.to_csv("../../out/TSV/%s.tsv" %(id), sep="\t", encoding="utf8", escapechar="\n", index=False)

