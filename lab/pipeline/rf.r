library(TreeDist)

args = commandArgs(trailingOnly=TRUE)
con_tree <- ape::read.tree(args[1])
tt_tree <- ape::read.tree(args[2])

# con_tree
#
# tt_tree

pdf(args[3], width = 12, height = 6)
VisualizeMatching(
                  RobinsonFouldsMatching,
                  con_tree,
                  tt_tree
)
title(main=args[4], sub=sprintf("normalised RF dist: %f", RobinsonFoulds(
                     con_tree,
                     tt_tree,
                     normalize = TRUE
                     )), line = 3)


