from typing import Iterator
from Bio import Entrez, SeqIO
from Bio.Entrez.Parser import DictionaryElement
from tqdm import tqdm
import sys

"""
Drzewa można osobno, ale analiza porównawcza w raporcie
"""

Entrez.email = "zuzanna.surd@gmail.com"

def id_generator(term: str) -> Iterator[str]:
    position = 0
    while True:
        handle = Entrez.esearch(db="protein", term=term, retstart=position, retmax=101)
        record = Entrez.read(handle)
        position += len(record["IdList"]) #type: ignore

        yield ",".join(record["IdList"])


N_GOAL = 101

# taxid -> item_id
found_ids: dict[int, str] = {}

bar = tqdm(id_generator("HBA1"), total=N_GOAL, desc="gathering ids")
for id in bar:
    handle=Entrez.efetch(db="protein", id=id, rettype="docsum")
    x = Entrez.read(handle)
    for item in x:
        taxid = int(item['TaxId'])
        if taxid not in found_ids:
            found_ids[taxid] = item['Id']
            bar.update(1)
    
            if len(found_ids) >= N_GOAL:
                break

    if len(found_ids) >= N_GOAL:
        break

fasta = Entrez.efetch(db="protein", id=",".join(found_ids.values()), rettype="fasta")

dist = sys.argv[1]
with open(dist, "w") as f:
    for line in tqdm(fasta, desc=f"saving to {dist}"):
        f.write(line)

