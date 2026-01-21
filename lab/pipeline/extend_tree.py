import re
from sys import argv
import sys
import pandas as pd


def full_tree_of_leaves(leaves: list[str]) -> str:
    aux = [None] * len(leaves) + leaves

    for i in range(2 * len(leaves) - 1, 0, -1):
        aux[i // 2] = (
            aux[i] if aux[i // 2] is None else f"({aux[i // 2]}:1, {aux[i]}:1)"
        )

    return aux[1] or "-"


def main(genomes_path: str, tree_file_path: str):
    names = [
        name.replace(" ", "_")
        for name in pd.read_csv(genomes_path, delimiter=";")["name"]
    ]
    taxa_name_re = re.compile(f"""({"|".join(names)})""")
    all_taxa: set[str] = set(names)
    with open(tree_file_path, "r") as f:
        tree = f.read().strip()[:-1]

    in_tree_taxa: set[str] = set(re.findall(taxa_name_re, tree))
    missing_taxa = all_taxa.difference(in_tree_taxa)

    print(f"""{tree_file_path=}\n{sorted(in_tree_taxa)}\n""")

    if len(missing_taxa) > 0:
        with open(tree_file_path, "w") as f:
            f.write(
                # (new_tree := f"({full_tree_of_leaves(list(missing_taxa))}:1,{tree}:1)")
                (
                    new_tree := f"(({','.join(f'{t}:1' for t in missing_taxa)}):1,{
                        tree
                    }:1)"
                )
                + ";"
            )

        print(
            f"""{tree_file_path=}\n{
                sorted(set(re.findall(taxa_name_re, new_tree)))
            }\n"""
        )

        tree = new_tree

    with open(tree_file_path, "w") as f:
        f.write(re.sub(r"\)$", f",DUMMY:{sys.maxsize})", tree) + ";")


if __name__ == "__main__":
    main(argv[1], argv[2])
