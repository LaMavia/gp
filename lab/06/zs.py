#!/usr/bin/env python3

import json
from time import sleep
import requests
from tqdm import tqdm

def download_sequence(accession: str):
    while True:
        res = requests.get(f"https://rest.uniprot.org/uniprotkb/{accession}.fasta")
        if res.status_code != 200:
            print("[ERROR] sleeping because: ", res.status_code)
            sleep(5)

        return "\n".join([f"> {accession}", *res.text.splitlines()[1:]])

def process_family(res: dict):
    protein_ids: list[str] = [r['metadata']['accession'] for r in res['results']][:30]
    
    with open("./out.fasta", "w") as f:
        for accession in tqdm(protein_ids):
            seq = download_sequence(accession)
            f.write("\n")
            f.write(seq)
                

def main():
    families: list[str] = [] 

    with open("./families.txt") as f:
        families = f.read().split(",")

    with open("./example-family.json") as f:
        res = json.load(f)

    process_family(res) 

if __name__ == "__main__":
    main()
