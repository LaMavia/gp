library(TreeDist)

#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)

print(args[1])
ape::read.tree(args[1])
