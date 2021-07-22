# Annotation d'un texte

## Lancement du script

## Que fait le script ?

### La segmentation

Le fichier encodé en XML-TEI est segmenté en plusieurs parties.
La ponctuation forte est utilisée pour procéder à cette segmentation.

Entrée : fichier XML-TEI
Sortie : fichier XML-TEI segmenté

### La lemmatisation

Le texte est ensuite lemmatisé et annoté morphosyntaxiquement en utilisant pie-extended.

PIE_EXTENDED_DOWNLOADS=~/MesModelsPieExtended python3 scripts/lemmatize.py file/to/path

Entrée : fichier XML-TEI segmenté
Sortie : fichier csv A

### La normalisation

Le texte est normalisé token par token (voir doc de Rachel).

Entrée : fichier XML-TEI segmenté
Sortie : fichier csv A (avec une nouvelle colonne)

### Reconstitution d'un fichier XML-TEI

À partir du fichier csv produit, le script ... permet de reconsituer un fichier XML-TEI reprenant toutes les informations d'annotations.