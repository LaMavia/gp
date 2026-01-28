CLUSTERS_DIR = ./clusters

.PHONY: clean

all: $(CLUSTERS_DIR)/%.treefile

tax_idx.txt: taxa.csv
	cat $^ | awk -F, 'NR>1 {{ print $$2 }}' > $@

protein.faa: tax_idx.txt
	rm -f ./ncbi_dataset.zip
	datasets --api-key $(NCBI_API_KEY) download genome accession --inputfile $^ --include protein 
	bash -c 'unzip -o ./ncbi_dataset.zip "*.faa"'
	cat ncbi_dataset/data/**/*.faa > $@
	# rm -rf ./ncbi_dataset
	# rm -f ./ncbi_dataset.zip

$(CLUSTERS_DIR): protein.faa taxa.csv
	mmseqs easy-cluster $< protein tmp \
		--min-seq-id 0.3 \
		--cov-mode 1\
		-v 1\
		-c 0.7
	rm -rf $(CLUSTERS_DIR)
	python3 ./spread_cluster_sequences.py ./taxa.csv $(CLUSTERS_DIR) ./protein_all_seqs.fasta
	python3 ./cluster_hist.py ./cluster_sizes.txt

$(CLUSTERS_DIR)/%.orth: $(CLUSTERS_DIR) taxa.csv
	find $(CLUSTERS_DIR) -name '*.faa' -print0 | python3 ./make_orth.py ./taxa.csv {}

$(CLUSTERS_DIR)/%.afa: $(CLUSTERS_DIR)/%.orth
	find $(CLUSTERS_DIR) -name '*.orth' -print0 |\
	parallel --progress -0 \
	muscle -align {} -output {.}.afa


$(CLUSTERS_DIR)/%.treefile: $(CLUSTERS_DIR)/%.afa 
	find $(CLUSTERS_DIR) -name "*.afa" -print0 |\
		parallel --progress -0 \
		iqtree3 --redo -T AUTO --fast -s {}

all_orth_trees.treefile: # $(CLUSTERS_DIR)/%.treefile
	find $(CLUSTERS_DIR) -name '*.treefile' -print0 |\
		parallel --progress -0 \
		cat {} > $@

orth_consensus.result.treefile: all_orth_trees.treefile
	iqtree3 -T AUTO --sup-min 0.5 -con $< $@

%.comparison.pdf: %.result.treefile publication.treefile 
	Rscript ./rf.r $^ $@ $*

clean:
	rm -f tax_ids.txt protein.faa protein_all_seqs.fasta *.fasta
	rm -rf $(CLUSTERS_DIR)

