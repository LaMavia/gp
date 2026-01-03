#!/usr/bin/env bash

t='iqtree-3.0.1-Linux/bin/iqtree3 -m JC -s ./species.afa -redo'
# t='VeryFastTree -nt ./species.afa > ./species.afa.treefile'

muscle -align ./species.fasta -output ./species.afa && \
bash -c "$t"



