#!/usr/bin/env bash

QUERIES_FILE=$1
SUBJECTS_FILE=$2

parallel --progress --link -a $QUERIES_FILE -a $SUBJECTS_FILE ./calc_blast.sh >/dev/null

