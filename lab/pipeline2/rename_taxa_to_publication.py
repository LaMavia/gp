import sys
import pandas as pd


def main(taxa_file: str, tree_file: str, output_tree_file: str):
    df = pd.read_csv(taxa_file)
    names = df["name"].to_list()
    seqnames = df["seqname"].to_list()

    with open(tree_file, "r") as f:
        tree = f.read()

    for seqname, name in zip(seqnames, names, strict=True):
        tree = tree.replace(seqname, name)

    with open(output_tree_file, "w") as f:
        f.write(tree)


if __name__ == "__main__":
    main(taxa_file=sys.argv[1], tree_file=sys.argv[2], output_tree_file=sys.argv[3])
