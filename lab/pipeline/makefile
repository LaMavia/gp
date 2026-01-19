all: genomes

clean:
	rm -rf ./sequences ./tmp ./clusters
	mkdir -p ./sequences ./clusters
	touch ./sequences/.gitkeep ./clusters/.gitkeep
	
	rm ./*.fasta ./*_cluster.tsv

family_sup_trees:


family_sub_trees:
	find ./clusters -name '*.afa' -print0 |\
		parallel --progress -0\
		iqtree3 --redo -s {}

family_naive_sub_trees:
	find ./clusters/ -name '*.afa' -print0 |\
		parallel --progress -0\
		python3 ./make_naive_trees.py {}

family_alignments:
	find ./clusters/ -name '*.fasta' -print0 |\
		parallel --progress -0 \
		muscle -align {} -output {.}.afa

cluster_dirs:
	find . -name '*_seqs.fasta' -print0 |\
		parallel --progress -0\
		python3 ./spread_cluster_sequences.py {} ./clusters

clusters:
	find ./sequences -iname '*.fasta' -print0 |\
		parallel --progress -0 \
		mmseqs easy-cluster {} {/.} tmp \
			--min-seq-id 0.5 \
			--cov-mode 0\
			--alignment-mode 4\
			-v 1\
			--add-self-matches 1\
			--cluster-mode 1

genomes:
	python3 ./download_genomes.py
