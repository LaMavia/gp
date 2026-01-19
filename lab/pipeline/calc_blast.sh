#!/usr/bin/env bash

QUERY=$1
SUBJECT=$2

QUERY_ID=$(basename "$QUERY")
SUBJECT_ID=$(basename "$SUBJECT")

if [[ "$QUERY" = "$SUBJECT" ]]; then 
  exit 0
fi

printf 'calculating BLAST for %s, %s\n' "$QUERY_ID" "$SUBJECT_ID"
blastn \
  -query "$QUERY" \
  -subject "$SUBJECT" \
  -out "./sequences/blast/${QUERY_ID%%.fasta}${SUBJECT_ID%%.fasta}.blast.xml"\
  -outfmt 5


