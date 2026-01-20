from sys import argv
from Bio import Phylo
from Bio.Phylo import NewickIO
from Bio.Phylo.Newick import Tree


def main(tree_file_path: str, out_file_path: str | None):
    with open(tree_file_path, "r") as f:
        tree: Tree = next(NewickIO.parse(f))

    tree.prune("DUMMY")
    new_tree = tree.format("newick").replace(":0.00000", "")

    if out_file_path is not None:
        with open(out_file_path, "w") as f:
            f.write(new_tree)
    else:
        print(new_tree, end="")


if __name__ == "__main__":
    main(argv[1], argv[2] if len(argv) > 2 else None)
