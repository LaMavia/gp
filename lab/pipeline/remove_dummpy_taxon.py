from sys import argv
from Bio import Phylo
from Bio.Phylo import NewickIO
from Bio.Phylo.Newick import Tree


def main(tree_file_path: str):
    with open(tree_file_path, "r") as f:
        tree: Tree = next(NewickIO.parse(f))

    tree.prune("DUMMY")
    with open(tree_file_path, "w") as f:
        f.write(tree.format("newick").replace(":0.00000", ""))


if __name__ == "__main__":
    main(argv[1])
