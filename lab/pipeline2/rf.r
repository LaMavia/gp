library(TreeDist)

# args: result_tree, publication_tree, output_file, title

printf <- function(...) invisible(print(sprintf(...)))
root <- function(...) ape::root(..., resolve.root=TRUE, outgroup="Ustilago_hordei")

args = commandArgs(trailingOnly=TRUE)

con_tree <- ape::read.tree(args[1])
tt_tree <- ape::read.tree(args[2])

pdf(args[3], width = 12, height = 7)
VisualizeMatching(
                  JaccardRobinsonFoulds,
                  con_tree,
                  tt_tree,
)
title(main=args[4], line=3)

printf("nRF: %f, nJRF: %f", RobinsonFoulds(con_tree, tt_tree, normalize = TRUE), JaccardRobinsonFoulds(con_tree, tt_tree, normalize = TRUE))


