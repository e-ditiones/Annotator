import sentencepiece as spm
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('model_path')
args = parser.parse_args()

# load model
sp = spm.SentencePieceProcessor(model_file=args.model_path)

# encode
for line in sys.stdin:
    print(' '.join(sp.encode(line.strip(), out_type=str)))
