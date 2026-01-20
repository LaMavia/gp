#!/usr/bin/env bash

for f in ./trees/*.treefile; do
  python3 ./remove_dummpy_taxon.py "$f"
done > trees.ph
