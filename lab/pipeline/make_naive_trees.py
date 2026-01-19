from os.path import dirname
import sys


def main(file_path: str):
    genomes = []
    with open(file_path, "r") as f:
        for line in f:
            if line.startswith(">"):
                genomes.append(line[1:].strip())

    with open(f"{file_path}.treefile", "w") as f:
        f.write(f"""({",".join(f"{g}:1" for g in genomes)});""")


if __name__ == "__main__":
    main(file_path=sys.argv[1])
