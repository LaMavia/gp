CLUSTERS_DIR = ./clusters
SUPPORT_THRESHOLD = 30
CORES = 16
CON_TREES = $(patsubst %,%_consensus,orth filtered_orth)
SUP_TREES = $(patsubst %,%_super,orth)
TREES = $(CON_TREES) $(SUP_TREES)
TT_TREES = $(TREES:%=tt_%)
RESULT_TREES = $(TREES:%=%.result.treefile)
RENAMED_TREES = $(TREES:%=%.renamed.treefile)
TT_RENAMED_TREES = $(patsubst %,tt_%,$(RENAMED_TREES))
NCBI_COMPARISONS = $(TREES:%=%-ncbi.comparison.pdf)
PUB_COMPARISONS = $(TREES:%=%-pub.comparison.pdf)
TT_COMPARISONS = $(TT_TREES:%=%-tt.comparison.pdf)
SUPER_JOINED_TREES = $(patsubst %,all_%_trees.treefile,orth)
MISSING_TT_TAXONS = Rhodotorula_glutinis,Sporobolomyces_roseus

.PHONY: clean zs438730.tar.gz

all: clusters_dir aligned_orthological_clusters aligned_paralog_clusters trees comparisons

tax_idx.txt: taxa.csv
	cat $^ | awk -F, 'NR>1 {{ print $$3 }}' > $@

protein.faa: tax_idx.txt
	rm -f ./ncbi_dataset.zip
	datasets --api-key $(NCBI_API_KEY) download genome accession --inputfile $< --include protein --dehydrated 
	unzip ncbi_dataset.zip -d ncbi_dataset/
	datasets --api-key $(NCBI_API_KEY) rehydrate --directory ncbi_dataset/
	cat ncbi_dataset/ncbi_dataset/data/**/*.faa > $@
	# rm -f ./ncbi_dataset.zip

clusters_dir: protein.faa taxa.csv
	mmseqs easy-cluster $< protein tmp \
		--min-seq-id 0.5 \
		--cov-mode 0 \
		--cluster-mode 1 \
		-v 1\
		-c 0.7
	rm -rf $(CLUSTERS_DIR)
	python3 ./spread_cluster_sequences.py ./taxa.csv $(CLUSTERS_DIR) ./protein_all_seqs.fasta
	python3 ./cluster_hist.py ./cluster_sizes.txt

orthological_clusters: taxa.csv
	find $(CLUSTERS_DIR) -name '*.faa' -print0 | python3 ./make_orth.py ./taxa.csv

aligned_orthological_clusters: orthological_clusters
	find $(CLUSTERS_DIR) -name '*.orth' -print0 |\
	parallel -j $(CORES) --bar --eta -0 \
	muscle -align {} -output {}.afa

paralog_clusters:
	find $(CLUSTERS_DIR) -name '*.faa' -print0 | python3 ./make_para.py ./taxa.csv

aligned_paralog_clusters: paralog_clusters
	find $(CLUSTERS_DIR) -name '*.para' -print0 |\
	parallel -j $(CORES) --bar --eta -0 \
	muscle -align {} -output {}.afa

trees: 
	find $(CLUSTERS_DIR) -name "*.afa" -print0 |\
		parallel -j $(CORES) --bar --eta -0 \
		iqtree3 \
			--redo \
			-T 1 \
			--mset LG+I+G4,Q.PFAM+I+G4,Q.PFAM+F+I+G4,Q.YEAST+I+G4,Q.YEAST+F+I+G4 \
			--cmin 3 \
			--cmax 4 \
			-B 1000 \
			--boot-trees \
			-s {} 

filtered_orth_trees.treefile:
	find $(CLUSTERS_DIR) -name "*.orth.afa" -print0 |\
		parallel -j $(CORES) --bar --eta -0 \
		iqtree3 \
			-T 1 \
			--mset LG+I+G4,Q.PFAM+I+G4,Q.PFAM+F+I+G4,Q.YEAST+I+G4,Q.YEAST+F+I+G4 \
			--cmin 3 \
			--cmax 4 \
			-t {}.ufboot \
			--tree-fix \
			--support {}.treefile
	find $(CLUSTERS_DIR) -name "*.ufboot.suptree" -print0 |\
		python3 ./filter_supported.py $(SUPPORT_THRESHOLD) |\
		parallel -j $(CORES) --bar --eta -0 \
		cat {} > $@

$(SUPER_JOINED_TREES): all_%_trees.treefile:
	find $(CLUSTERS_DIR) -name '*$*.afa.treefile' -print0 |\
		parallel -j $(CORES) --bar --eta -0 \
		cat {} > $@

orth_consensus.result.treefile: all_orth_trees.treefile
	iqtree3 -T AUTO --sup-min 0.0 -con $< $@

filtered_orth_consensus.result.treefile: filtered_orth_trees.treefile 
	iqtree3 -T AUTO --sup-min 0.0 -con $< $@

orth_super.result.treefile:  
	clann -ln -c orth_clann_commands.txt
	sed -i 's/\[.*\]//' ./Heuristic_result.txt
	sed -i '2,$$ d' ./Heuristic_result.txt
	mv ./Heuristic_result.txt $@

$(RENAMED_TREES): %.renamed.treefile: %.result.treefile
	python3 ./rename_taxa_to_publication.py taxa.csv $< $@

$(TT_RENAMED_TREES): tt_%: %
	python3 ./remove_missing_taxons.py $< $@ $(MISSING_TT_TAXONS)
	sed -i 's/:\\d*\\.\\d*//' $@

$(NCBI_COMPARISONS): %-ncbi.comparison.pdf: %.renamed.treefile ncbi.phy
	Rscript ./rf.r $^ $@ "$* vs. NCBI"

$(PUB_COMPARISONS): %-pub.comparison.pdf: %.renamed.treefile publication.treefile
	Rscript ./rf.r $^ $@ "$* vs. Publication"

$(TT_COMPARISONS): %-tt.comparison.pdf: %.renamed.treefile tt.treefile
	Rscript ./rf.r $^ $@ "$* vs. TimeTree"

comparisons: $(NCBI_COMPARISONS) $(PUB_COMPARISONS) $(TT_COMPARISONS)

clean:
	rm -f tax_idx.txt protein.faa protein_all_seqs.fasta *.fasta *.*.treefile all*.treefile* cluster_sizes.* ncbi_dataset.zip protein_* *.log proteom_ids.txt md5sum.txt 
	rm -rf $(CLUSTERS_DIR) ncbi_dataset tmp

gene_trees.treefile:
	find $(CLUSTERS_DIR) -name  '*.treefile' -print0 |\
		parallel --bar --eta -0 cat {} > $@

zs438730.tar.gz: $(wildcard *.csv) orth_clann_commands.txt README.md makefile $(wildcard raport/*) $(wildcard *.nix) $(wildcard *.py) $(wildcard *.pdf) $(wildcard *.renamed.treefile) $(wildcard *.sh) 
	GZIP=-9 tar -czf  $@ $^

