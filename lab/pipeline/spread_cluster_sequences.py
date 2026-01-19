from collections import defaultdict
from itertools import pairwise
from os import mkdir, path
from pathlib import Path
import re
import sys


def main():
    _, file_path, clusters_dir = sys.argv
    dirname = f"{clusters_dir}/{Path(file_path).stem}"

    try:
        mkdir(dirname)
    except Exception:
        pass

    with open(file_path, "r") as f:
        lines = f.readlines()
        header_lines = {i for i, (a, b) in enumerate(pairwise(lines)) if a == b}

        groups = defaultdict(list)
        group = None
        for i, line in enumerate(lines):
            if i in header_lines:
                group = line[1:].strip()
            else:
                groups[group].append(line)

        print(*((k, len(v)) for k, v in groups.items()), sep="\n")

    for g, lines in groups.items():
        with open(f"{dirname}/{g}.fasta", "w") as f:
            f.writelines(lines)


if __name__ == "__main__":
    main()
