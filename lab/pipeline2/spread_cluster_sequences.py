from collections import defaultdict
from itertools import pairwise
from os import mkdir
import sys


def main():
    _, taxa_file, clusters_dir, file_path = sys.argv

    with open(taxa_file, "r") as f:
        for expected_taxa, _ in enumerate(f):
            pass

    try:
        mkdir(clusters_dir)
    except Exception:
        pass

    with open(file_path, "r") as f:
        lines = f.readlines()
        header_lines = {
            i
            for i, (a, b) in enumerate(pairwise(lines))
            if a.startswith(">") and b.startswith(">")
        }

        groups = defaultdict(list)
        group = None
        for i, line in enumerate(lines):
            if i in header_lines:
                group = line[1:].strip()
            else:
                groups[group].append(line)

        gs = sorted([(k, len(v)) for k, v in groups.items()], key=lambda p: p[1])

        with open("cluster_sizes.txt", "w") as f:
            for _, size in gs:
                f.write(f"{size}\n")

    for g, lines in groups.items():
        with open(f"{clusters_dir}/{g}.faa", "w") as f:
            f.writelines(lines)


if __name__ == "__main__":
    main()
