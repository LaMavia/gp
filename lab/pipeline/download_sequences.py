import sys
from Bio import SeqIO, Entrez
import pandas as pd
from tqdm import tqdm

Entrez.email = "zs438730@students.mimuw.edu.pl"


def download_by_id(id: str, tag: str, sequences_dir: str):
    handle = Entrez.efetch(db="nucleotide", id=id, rettype="fasta")
    with open(out_path := f"{sequences_dir}/seq.fasta", "a") as f:
        f.writelines(
            [f">{id}\n", str(SeqIO.read(handle, "fasta").translate().seq), "\n"]
        )

    return out_path


def main():
    _, query_file_path, subject_file_path = sys.argv

    csv = pd.read_csv("./genomes.csv", delimiter=";")
    names = list(csv["name"])
    ids = list(csv["id"])
    bar = tqdm(zip(ids, names), desc="downloading sequences", total=len(names))
    output_paths = []
    for id, name in bar:
        bar.set_postfix_str(f"{name}, {id}")
        output_paths.append(
            download_by_id(id=id, tag=name, sequences_dir="./sequences/genomes")
        )

    with (
        open(query_file_path, "w") as query_file,
        open(subject_file_path, "w") as subject_file,
    ):
        for i, query in enumerate(output_paths):
            for j, subject in enumerate(output_paths):
                if j < i:
                    query_file.write(f"{query}\n")
                    subject_file.write(f"{subject}\n")


if __name__ == "__main__":
    main()
