import sys
from tqdm.contrib.concurrent import thread_map
import re

support_value_re = re.compile(r"\d+\/\d+")

SUPPORT_THRESHOLD = int(sys.argv[1])


def tree_support_values(tree: str):
    return (
        tuple(int(v) for v in m.group(0).split("/"))
        for m in re.finditer(support_value_re, tree)
        if len(m.group(0)) > 0
    )


def filter_tree(support_file: str):
    with open(support_file, "r") as f:
        tree = f.read()

    if all(
        bs > SUPPORT_THRESHOLD and shaltrs > SUPPORT_THRESHOLD
        for bs, shaltrs in tree_support_values(tree)
    ):
        return support_file.replace(".ufboot.suptree", ".treefile")


def main(support_files: list[str]):
    print(
        "\000".join(t for t in thread_map(filter_tree, support_files) if t is not None),
        end="",
    )


if __name__ == "__main__":
    main([f for f in input().split("\000") if len(f) > 0])
