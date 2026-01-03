library(TreeDist)

own_tree <- ape::read.tree("./species.afa.treefile")
tt_tree <- ape::read.tree("./species.tt.nwk")

own_tree

tt_tree

# pdf("./Rplots2.pdf", width = 12, height = 6)
# matching <- VisualizeMatching(
#                   RobinsonFouldsMatching,
#                   own_tree,
#                   tt_tree
# )
# title("Own tree vs. TimeTree", line = 3)
# sprintf("RF dist: %f", RobinsonFoulds(
#                      own_tree,
#                      tt_tree,
#                      normalize = TRUE
#                      ))
#
# print(attributes(matching))
