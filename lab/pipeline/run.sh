#!/usr/bin/env bash

make -B genomes
make -B clusters
make -B cluster_dirs
make -B family_alignments 
make -B family_naive_sub_trees
make -B family_sub_trees
make -B sup_alignments
make -B naive_sup_trees
make -B sup_trees
make -B --keep-going trees 
make -B consensus
make -B supertree
