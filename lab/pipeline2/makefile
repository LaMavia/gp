CLUSTERS_DIR = ./clusters

.PHONY: clean

all: $(CLUSTERS_DIR)/%.orth

tax_idx.txt: taxa.csv
	cat $^ | awk -F, 'NR>1 {{ print $$2 }}' > $@

protein.faa: tax_idx.txt
	rm -f ./ncbi_dataset.zip
	datasets --api-key $(NCBI_API_KEY) download genome accession --inputfile $^ --include protein 
	bash -c 'unzip -o ./ncbi_dataset.zip *.faa'
	cat ncbi_dataset/data/**/*.faa > $@
	# rm -rf ./ncbi_dataset
	# rm -f ./ncbi_dataset.zip

$(CLUSTERS_DIR): protein.faa taxa.csv
	mmseqs easy-cluster $< protein tmp \
		--min-seq-id 0.3 \
		--cov-mode 3\
		-v 1\
		-c 0.7
	rm -f $(CLUSTERS_DIR)
	python3 ./spread_cluster_sequences.py ./taxa.csv $(CLUSTERS_DIR) ./protein_all_seqs.fasta
	python3 ./cluster_hist.py ./cluster_sizes.txt

$(CLUSTERS_DIR)/%.orth: $(CLUSTERS_DIR) taxa.csv
	find $(CLUSTERS_DIR) -name '*.faa' -print0 | python3 ./make_orth.py ./taxa.csv {}

clean:
	rm -f tax_ids.txt protein.faa protein_all_seqs.fasta *.fasta
	rm -rf $(CLUSTERS_DIR)

