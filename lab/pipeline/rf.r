library(TreeDist)

args = commandArgs(trailingOnly=TRUE)
own_tree <- ape::read.tree(args[1])
tt_tree <- ape::read.tree(args[2])

# own_tree
#
# tt_tree

pdf("./Rplots2.pdf", width = 12, height = 6)
VisualizeMatching(
                  RobinsonFouldsMatching,
                  own_tree,
                  tt_tree
)
title("Consensus vs. Publication", line = 3)
sprintf("normalised RF dist: %f", RobinsonFoulds(
                     own_tree,
                     tt_tree,
                     normalize = TRUE
                     ))

