library("ggtree")

tree <- read.tree("out.nwk")

pdf("./Tree.pdf", width=300, height=20)

ggplot(tree, branch.length='none') + 
  layout_dendrogram() +
  geom_tree() + 
  theme_tree()
