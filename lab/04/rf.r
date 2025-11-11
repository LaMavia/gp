library(TreeDist)

own_tree <- ape::read.tree("./species.afa.treefile")
tt_tree <- ape::read.tree("./species.nwk")

# tree1 <- ape::read.tree(text = '(A, ((B, (C, (D, E))), ((F, G), (H, I))));')
# tree2 <- ape::read.tree(text = '(A, ((B, (C, (D, (H, I)))), ((F, G), E)));')


pdf('./Rplots2.pdf', width=12, height=6)
VisualizeMatching(
                  JaccardRobinsonFoulds, 
                  own_tree, 
                  tt_tree,
                  matchZeros = FALSE)
# plot(own_tree)
# SharedPhylogeneticInfo(own_tree, tt_tree)
# VisualizeMatching(MatchingSplitDistance, own_tree, tt_tree, 
#                   Plot = TreeDistPlot, matchZeros = FALSE)
