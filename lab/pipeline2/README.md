# Pipeline filogenetyczny

Do uruchomienia wymagane są programy:

- iqtree3
- clann
- python3 (pakiety: tqdm, biopython, altair, pandas, vl-convert-python)
- make
- parallel (gnu-parallel)
- Rscript (pakiety: TreeDist)
- mmseqs (v2)
- muscle

oraz zmienna środowiskowa `NCBI_API_KEY`.

Dostępny jest plik `flake.nix`, wymagający pliku `.env` ze zmienną `NCBI_API_KEY`.

Do uruchomienia powinno wystarczyć polecenia `make`.
