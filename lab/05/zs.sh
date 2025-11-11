#!/usr/bin/env bash

fasta_dist="./sequences.fa"
mfa_dist="./sequences.mfa"

if [ -f "$mfa_dist" ]; then
  rm "$mfa_dist"
fi

printf 'Downloading sequences\n'
python3 ./zs.py "$fasta_dist"

printf 'Aligning\n'
muscle -align "$fasta_dist" -output "$mfa_dist"
