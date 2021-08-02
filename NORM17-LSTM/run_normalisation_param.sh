#!/bin/sh

text="$1"

if [ $# -ne 1 ]; then
    echo "Error: text must be provided as a parameter. Make sure to surround the text with quotes."
    exit
fi

thisdir=`dirname $0`
pid=$$ # get process id to use to name files to avoid conflict in cases of parallelisation

# pre-normalisation, apply sentencepiece
echo "$text" | bash pre-norm.sh > $thisdir/model/input.$pid
cat $thisdir/model/input.$pid | python encode_sp.py $thisdir/model/bpe_joint_1000.model > $thisdir/model/input.preproc.$pid

# normalisation using fairseq model
cat $thisdir/model/input.preproc.$pid | fairseq-interactive \
				    --path $thisdir/model/checkpoint_bestwordacc_sym.pt \
				    $thisdir/model --remove-bpe sentencepiece \
				    -s src -t trg \
				    > $thisdir/model/output.$pid 2> /dev/null

# postprocess
cat $thisdir/model/output.$pid | grep "H-" | perl -pe 's/^H-//' | sort -n | cut -f 3 > $thisdir/model/output.postproc.$pid

# align to original text
python $thisdir/align/align.py $thisdir/model/input.$pid $thisdir/model/output.postproc.$pid

# remove temporary files
rm $thisdir/model/input.$pid
rm $thisdir/model/input.preproc.$pid
rm $thisdir/model/output.$pid
rm $thisdir/model/output.postproc.$pid