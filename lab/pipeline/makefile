all: genomes

clean:
	rm -rf ./sequences ./tmp ./clusters ./trees
	mkdir -p ./sequences ./clusters ./trees
	touch ./sequences/.gitkeep ./clusters/.gitkeep ./trees/.gitkeep
	
	rm ./*.fasta ./*_cluster.tsv

trees:
	find . -depth -maxdepth 1 -name '*_rep_seq.afa.treefile' -print0 |\
		parallel --progress --plus -0 \
		python3 ./substitute_family_trees.py \
			{} \
			./clusters/{%_rep_seq.afa.treefile}_all_seqs \
			./trees

	find ./trees -name '*.treefile' -print0 |\
		parallel --progress -0 \
		python3 ./extend_tree.py ./genomes.csv {}

	cat ./trees/*.treefile > all_trees.treefile

sup_trees:
	find . -name '*_rep_seq.afa' -print0 |\
		parallel --progress -0\
		iqtree3 --redo -s {}

naive_sup_trees:
	find . -name '*_rep_seq.afa' -print0 |\
		parallel --progress -0\
		python3 ./make_naive_trees.py {}

sup_alignments:
	find . -name '*_rep_seq.fasta' -print0 |\
		parallel --progress -0 \
		muscle -align {} -output {.}.afa

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
