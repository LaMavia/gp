CLUSTERS_DIR = ./clusters

.PHONY: clean comparison

all: $(CLUSTERS_DIR)/%.treefile

tax_idx.txt: taxa.csv
	cat $^ | awk -F, 'NR>1 {{ print $$3 }}' > $@

protein.faa: tax_idx.txt
	rm -f ./ncbi_dataset.zip
	datasets --api-key $(NCBI_API_KEY) download genome accession --inputfile $^ --include protein --dehydrated 
	unzip ncbi_dataset.zip -d ncbi_dataset/
	datasets --api-key $(NCBI_API_KEY) rehydrate --directory ncbi_dataset/
	cat ncbi_dataset/ncbi_dataset/data/**/*.faa > $@
	# rm -f ./ncbi_dataset.zip

$(CLUSTERS_DIR): protein.faa taxa.csv
	mmseqs easy-cluster $< protein tmp \
		--min-seq-id 0.5 \
		--cov-mode 1\
		-v 1\
		-c 0.8
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
		iqtree3 \
			--redo \
			-T 1 \
			--mset LG+I+G4,Q.PFAM+I+G4,Q.PFAM+F+I+G4,Q.YEAST+I+G4,Q.YEAST+F+I+G4 \
			--cmin 3 \
			--cmax 4 \
			-B 1000 \
			-s {}

all_orth_trees.treefile: $(CLUSTERS_DIR)/%.treefile
	find $(CLUSTERS_DIR) -name '*.treefile' -print0 |\
		parallel --progress -0 \
		cat {} > $@

orth_consensus.result.treefile: all_orth_trees.treefile
	iqtree3 -T AUTO --sup-min 0.0 -con $< $@

%.renamed.treefile: %.result.treefile taxa.csv 
	python3 ./rename_taxa_to_publication.py taxa.csv $< $@

%-publication.comparison.pdf: %.renamed.treefile publication.treefile 
	Rscript ./rf.r $^ $@ $*

%-ncbi.comparison.pdf: %.renamed.treefile ncbi.phy
	Rscript ./rf.r $^ $@ $*

comparison: 
	rm -f *.comparison.pdf
	$(MAKE) orth_consensus-publication.comparison.pdf
	$(MAKE) orth_consensus-ncbi.comparison.pdf

clean:
	rm -f tax_idx.txt protein.faa protein_all_seqs.fasta *.fasta *.*.treefile all*.treefile* cluster_sizes.* ncbi_dataset.zip protein_* *.log proteom_ids.txt md5sum.txt 
	rm -rf $(CLUSTERS_DIR) ncbi_dataset

