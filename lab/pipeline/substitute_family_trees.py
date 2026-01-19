import os
from pathlib import Path
import sys


def get_tree(file_path: str) -> tuple[str, str]:
    with open(file_path, "r") as f:
        return Path(file_path).stem.split(".")[0], f.read()[:-1]


def get_family_trees(family_tree_file_dir: str) -> dict[str, str]:
    files = os.listdir(family_tree_file_dir)
    return {
        (t := get_tree(f"{family_tree_file_dir}/{f}"))[0]: t[1]
        for f in files
        if f.endswith(".treefile")
    }


def main(sup_tree_file: str, family_tree_file_dir: str, dist_dir: str):
    name, sup_tree = get_tree(sup_tree_file)
    family_trees = get_family_trees(family_tree_file_dir)

    for gene, gene_tree in family_trees.items():
        sup_tree = sup_tree.replace(f"{gene}:", f"{gene_tree}:")

    with open(f"{dist_dir}/{name}.treefile", "w") as f:
        f.write(sup_tree)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
