from sys import argv
import pandas as pd
import re
from collections import deque
import multiprocessing as mp
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map  # or thread_map

taxon_regex = re.compile(r".*\[([^\]]*)\]$")


def process_file(datum: tuple[int, str]):
    expected_num_taxons, file = datum

    out_file = f"{file}.orth"
    taxon_proteon_map: dict[str, str] = {}

    if file_length(file) // 2 < expected_num_taxons:
        # print(f"[{file}] exiting, too short")
        return

    with open(file, "r") as f:
        taxon: str | None = None
        for line in f:
            if line.startswith(">"):
                if (m := re.match(taxon_regex, line)) is None:
                    raise ValueError(line)
                taxon = m.group(1)

            elif taxon is not None:
                taxon_proteon_map[taxon] = (
                    line.rstrip()
                    if taxon_proteon_map.get(taxon) is None
                    else max(taxon_proteon_map[taxon], line.rstrip(), key=len)
                )

    if len(taxon_proteon_map) < expected_num_taxons:
        # print(f"[{file}] exiting, not 1-1")
        return taxon_proteon_map

    with open(out_file, "w") as f:
        for taxon, proteom in taxon_proteon_map.items():
            f.write(f">{taxon.replace(' ', '_')}\n{proteom}\n")

    print(f"[{file}] OK")

    return taxon_proteon_map


def file_length(file: str):
    with open(file, "r") as f:
        return deque(enumerate(f), maxlen=1)[0][0] + 1


def main(taxa_file: str, files: list[str]):
    expected_num_taxons = len(set(pd.read_csv(taxa_file)["name"]))

    vs = process_map(
        process_file, [(expected_num_taxons, file) for file in files], max_workers=16
    )
    print(
        *sorted([sorted(list(v.keys())) for v in vs if v is not None], key=len),
        sep="\n\n",
    )


if __name__ == "__main__":
    main(argv[1], [f for f in input().split("\000") if len(f) > 0])
