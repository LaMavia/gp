import sys
from Bio.Phylo import NewickIO


def main(in_file: str, out_file: str, taxons: list[str]):
    with open(in_file, "r") as f:
        tree = next(NewickIO.parse(f))

    for taxon in taxons:
        tree.prune(taxon)

    with open(out_file, "w") as f:
        NewickIO.write([tree], f, plain=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], [t.strip() for t in sys.argv[3].split(",")])
