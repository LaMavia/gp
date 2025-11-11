#!/usr/bin/env bash

muscle -align ./species.fasta -output ./species.afa && \
iqtree-3.0.1-Linux/bin/iqtree3 -s ./species.afa -redo && \
Rscript ./rf.r
