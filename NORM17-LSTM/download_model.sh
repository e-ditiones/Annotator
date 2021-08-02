#!/bin/sh

# make sure to unpack in the current directory
thisdir=`realpath $(dirname $0)`
cd $thisdir

wget http://almanach.inria.fr/files/modfr_norm/lstm_best/model.tar.gz
tar -xzvf model.tar.gz

rm -r model.tar.gz
