from collections import defaultdict
from io import TextIOWrapper
from itertools import groupby
import re
import sys
from typing import Optional
from Bio import SeqIO, Entrez, Seq
import pandas as pd
import json
from tqdm import tqdm

Entrez.email = "zs438730@students.mimuw.edu.pl"

GENOMES_DIR = "genomes"

POLY_GENE = "ORF 1a/1b"

GENE_NAME_MAP_RAW = {
    POLY_GENE: {
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
        "replicase 1a",
        "replicase 1b",
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
    "HE": {"HE", "hemmaglutinin-esterase", "HE protein"},
}

SUB_FEATURES_RAW = {
    "*PL": r".+CoV_PLPro$",
    "CPL": r"^(CoV_PLPro|CoV_peptidase|Peptidase_C16)$",
    "Hel": r".*13-helicase$",
    "Pol": r".*RdRp.*",
    "3CL": r".*_Nsp5_Mpro$",
}

SUB_FEATURES = {g: re.compile(r) for g, r in SUB_FEATURES_RAW.items()}

GENE_DISAMB = {"N": lambda p: p[2] > 1000, "ORF 1a/1b": lambda p: p[2] > 20_000}

PROTEIN_ID_REDIRECT = {"NP_937947.2": "NP_937947.1", "YP_209229.1": "YP_209229.2"}


def lookup_sub_feature(key: str) -> Optional[str]:
    for gene, key_regex in SUB_FEATURES.items():
        if key_regex.match(key) is not None:
            return gene

    return None


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


def find_assoc_exc(
    assoc: list, keys: list[tuple[str, str]], val_key: str
) -> str | None:
    for item in assoc:
        for kk, kv in keys:
            if kk in item and item[kk] == kv:
                return item[val_key]

    return None


def spread_subfeature(
    gene: tuple[str, set[tuple[str, int, int]]],
) -> dict[str, set[tuple[str, int, int]]]:
    name, subs = gene
    if len(subs) <= 1:
        return {name: subs}

    a, b = sorted(subs, key=lambda x: x[1])

    if b[1] <= a[2]:
        if a[2] - a[1] > b[2] - b[1]:
            return {"CPL": {a}}
        return {"CPL": {b}}

    return {"CPL": {a}, "*PL": {b}}


def extract_subfeatures(
    protein_id: str,
) -> list[tuple[str, str, int, int]]:  # name, seq, start, end
    handle = Entrez.efetch(db="protein", id=protein_id, rettype="xml")
    x = Entrez.read(handle)
    features = []

    for item in x:
        seq = item["GBSeq_sequence"]

        for feature in item["GBSeq_feature-table"]:
            if feature["GBFeature_key"] == "Region":
                raw_region_name = (
                    find_assoc_exc(
                        feature["GBFeature_quals"],
                        [("GBQualifier_name", "region_name")],
                        "GBQualifier_value",
                    )
                    or ""
                )
                if (gene := lookup_sub_feature(raw_region_name)) is None:
                    continue

                location = feature["GBFeature_location"]
                p, q = parse_location(location)

                features.append((gene, seq[p : q + 1], p, q))

    return features


def download_by_id(id: str):
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

    poly_protein_ids = []

    for item in x:
        nuc_seq = item["GBSeq_sequence"]
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
                protein_id = (
                    find_assoc_exc(
                        feature["GBFeature_quals"],
                        [("GBQualifier_name", "protein_id")],
                        "GBQualifier_value",
                    )
                    or ""
                )
                translation = (
                    find_assoc_exc(
                        feature["GBFeature_quals"],
                        [("GBQualifier_name", "translation")],
                        "GBQualifier_value",
                    )
                    or ""
                )
                p, q = parse_location(location)

                gene = (
                    GENE_NAME_MAP.get(normalize_key(gene))
                    or GENE_NAME_MAP.get(normalize_key(product))
                    or GENE_NAME_MAP.get(normalize_key(note))
                )

                if gene == POLY_GENE:
                    poly_protein_ids.append(
                        PROTEIN_ID_REDIRECT.get(protein_id, protein_id)
                    )
                elif gene is not None:
                    genes.append(
                        (
                            gene,
                            translation.lower()
                            if translation is not None
                            else Seq.translate(
                                nuc_seq[p : q + 1], stop_symbol=""
                            ).lower(),
                            p,
                            q,
                        )
                    )

        gene_groups = defaultdict(list)
        for p in genes:
            gene_groups[p[0]].append(p[1:])

        genes = {}
        for g, ps in gene_groups.items():
            if len(ps) > 1:
                genes[g] = [p for p in ps if GENE_DISAMB[g]][0]
            else:
                genes[g] = ps[0]

        raw_protein_features = defaultdict(set)
        for protein_id in poly_protein_ids:
            for gene, seq, p, q in extract_subfeatures(protein_id):
                raw_protein_features[gene].add((seq, p, q))

        protein_features = {}
        for f in raw_protein_features.items():
            protein_features.update(spread_subfeature(f))

        protein_features = {k: list(v)[0] for k, v in protein_features.items()}

        return {**genes, **protein_features}


def main():
    csv = pd.read_csv("./genomes.csv", delimiter=";")
    names = [n.replace(" ", "_") for n in csv["name"]]
    ids = list(csv["id"])
    gene_files: dict[str, TextIOWrapper] = {}
    bar = tqdm(list(zip(ids, names)), desc="Downloading genes")

    for id, name in bar:
        bar.set_postfix_str(name)
        if (genes := download_by_id(id=id)) is None:
            continue

        for gene, (seq, _, _) in genes.items():
            if gene not in gene_files:
                gene_files[gene] = open(f"sequences/{gene}.fasta", "w")

            gene_files[gene].write(f">{name}\n{seq}\n")

    for f in gene_files.values():
        f.flush()
        f.close()


if __name__ == "__main__":
    main()
