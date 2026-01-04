from collections import defaultdict
from itertools import groupby
import re
import sys
from typing import Optional
from Bio import SeqIO, Entrez
import pandas as pd
import json

Entrez.email = "zs438730@students.mimuw.edu.pl"

GENOMES_DIR = "genomes"

GENE_NAME_MAP_RAW = {
    "ORF 1a/1b": {
        "ORF 1a/1b",
        "orf1ab polyprotein",
        "replicase polyprotein 1ab",
        "ORF1ab",
        "ORF1 polyprotein",
        "ORF1ab polyprotein",
        "replicase polyprotein",
        "1ab",
        "ORF 1ab polyprotein",
        "Pol1",
    },
    "S": {
        "S",
        "spike protein",
        "spike glycoprotein",
        "spike glycoprotein (S)",
        "surface glycoprotein",
    },
    # "nsp 3a": {
    #     "nsp 3a",
    #     "non-structural protein 3a",
    #     "3a",
    #     "ns3",
    #     "NS3",
    #     "putative 3a protein",
    # },
    "E": {
        "E",
        "E protein",
        "envelope protein",
        "small membrane protein",
        "envelop protein (E)",
        "small envelope protein",
        "small virion-associated protein",
        """nonstructural 9.5 kDa protein; envelope protein;
                     small membrane protein""",
    },
    "M": {
        "M",
        "matrix protein",
        "membrane protein",
        "membrane glycoprotein",
        "M protein",
        "membrane protein (M)",
        "membrane glycoprotein M",
        "matrix glycoprotein",
    },
    "N": {
        "N",
        "nucleocapsid protein",
        "nucleoprotein",
        "nucleocapsid protein (N)",
        "nucleocapsid phosphoprotein",
    },
}

GENE_DISAMB = {"N": lambda p: p[2] > 1000, "ORF 1a/1b": lambda p: p[2] > 20_000}


def normalize_key(k: str | None) -> str | None:
    if k is None:
        return None

    return k.lower().replace(" ", "").replace("\n", "")


GENE_NAME_MAP = {
    normalize_key(synonym): gene
    for gene, synonyms in GENE_NAME_MAP_RAW.items()
    for synonym in synonyms
}


def parse_location(loc: str) -> tuple[int, int]:
    if loc.startswith("join"):
        locations = [parse_location(ll) for ll in loc[5:-1].split(",")]
        p = min(p for p, _ in locations)
        q = max(q for _, q in locations)
        return p, q

    ps, qs = loc.split("..")
    return int(ps.strip("<>")), int(qs.strip("<>"))


def find_assoc_exc[T](
    assoc: list, keys: list[tuple[str, str]], val_key: str
) -> str | None:
    for item in assoc:
        for kk, kv in keys:
            if kk in item and item[kk] == kv:
                return item[val_key]

    return None


def download_by_id(id: str, tag: str, sequences_dir: str):
    # pat = re.compile(r"[\s\t\n]*")
    # print(f"\n{id=}")
    # print("")
    handle = Entrez.efetch(db="nucleotide", id=id, rettype="xml")
    # print(f">{tag}")
    # print(str(SeqIO.read(handle, "fasta").seq))
    x = Entrez.read(handle)
    if x is None:
        print("NONE")
        return None

    # if id == "DQ811787":
    #     print(json.dumps(x, indent=2), file=sys.stderr)
    dq_poses = []

    seqlen = 0
    for item in x:
        seqlen = len(item["GBSeq_sequence"])
        genes = []
        for feature in item["GBSeq_feature-table"]:
            if feature["GBFeature_key"] == "CDS":
                # print(json.dumps(feature["GBFeature_quals"], indent=2))
                location = feature["GBFeature_location"]
                gene = find_assoc_exc(
                    feature["GBFeature_quals"],
                    [("GBQualifier_name", "gene")],
                    "GBQualifier_value",
                )
                product = find_assoc_exc(
                    feature["GBFeature_quals"],
                    [("GBQualifier_name", "product")],
                    "GBQualifier_value",
                )
                note = find_assoc_exc(
                    feature["GBFeature_quals"],
                    [("GBQualifier_name", "note")],
                    "GBQualifier_value",
                )
                p, q = parse_location(location)

                og_gene = gene
                gene = (
                    GENE_NAME_MAP.get(normalize_key(gene))
                    or GENE_NAME_MAP.get(normalize_key(product))
                    or GENE_NAME_MAP.get(normalize_key(note))
                )

                if (
                    id == "DQ811787"
                    and product is not None
                    and product.startswith("replicase")
                ):
                    dq_poses.append((p, q))

                if gene is not None:
                    genes.append((gene, p, q))
                    # print(f"{location};{q - p + 1};{gene}")
                # print({"length": q - p + 1, "g": gene, "p": product, "n": note})

        if id == "DQ811787":
            p = min(lp for lp, _ in dq_poses)
            q = max(lq for _, lq in dq_poses)
            genes.append(("ORF 1a/1b", p, q))

        gene_groups = defaultdict(list)
        for p in genes:
            gene_groups[p[0]].append(p)

        genes = {}
        for g, ps in gene_groups.items():
            if len(ps) > 1:
                genes[g] = [p for p in ps if GENE_DISAMB[g]][0]
            else:
                genes[g] = ps[0]

        print(f"{id};{seqlen}", end="")
        gs = ["E", "M", "N", "ORF 1a/1b", "S"]
        # prefixes = [normalize_key(g) for g in gs]
        for g in gs:
            # pref = normalize_key(g)
            if (p := genes.get(g)) is not None:
                _, s, e = p
                print(f";{s};{e}", end="")
            else:
                print(r";\N;\N", end="")

        print("")
        # for g, loc, ln in sorted(genes, key=lambda p: p[0]):
        #     print(f";{g};{ln};{loc}")


def main():
    gs = ["E", "M", "N", "ORF 1a/1b", "S"]
    prefs = ["e", "m", "n", "orf", "s"]
    print("name;id;seqlen", end="")
    for g, pref in zip(gs, prefs):
        # pref = normalize_key(g)
        print(f";{pref}_start;{pref}_end", end="")
    print("")
    csv = pd.read_csv("./genomes.csv", delimiter=";")
    names = list(csv["name"])
    ids = list(csv["id"])
    for id, name in zip(ids, names):
        print(f"{name};", end="")
        download_by_id(id=id, tag="", sequences_dir="")


if __name__ == "__main__":
    main()
