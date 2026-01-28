library(TreeDist)

# args: result_tree, publication_tree, output_file, title

args = commandArgs(trailingOnly=TRUE)
con_tree <- ape::root(ape::read.tree(args[1]), outgroup="Ustilago hordei")
tt_tree <- ape::root(ape::read.tree(args[2]), outgroup="Ustilago hordei")

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


