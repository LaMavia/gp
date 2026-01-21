all: genomes clusters cluster_dirs trees consensus supertree

clean:
	rm -rf ./sequences ./tmp ./clusters ./trees
	mkdir -p ./sequences ./clusters ./trees
	touch ./sequences/.gitkeep ./clusters/.gitkeep ./trees/.gitkeep
	
	rm -f ./*.fasta ./*_cluster.tsv
	rm -f ./*.afa* ./cmp1.* ./con.* ./all_trees.* ./*.log ./*.rfdist ./*.ps ./*.ph ./Heuristic_result.txt ./*.pdf ./*.nex

supertree:
	./make_ph.sh
	clann -ln -c clann_commands.txt
	sed -i 's/\[.*\]//' ./Heuristic_result.txt
	sed -i '2,$$ d' ./Heuristic_result.txt
	Rscript ./rf.r ./Heuristic_result.txt ./publication.treefile ./sup.pdf "Supertree vs. Publication"

consensus: all_trees.treefile
	iqtree3 -T AUTO --sup-min 0.3 -con ./all_trees.treefile ./con.treefile
	python3 ./remove_dummpy_taxon.py ./con.treefile ./con.treefile
	Rscript ./rf.r ./con.treefile ./publication.treefile ./con.pdf "Consensus vs. Publication"

all_trees.treefile:
	cat ./trees/*.treefile > all_trees.treefile
	# find ./trees/ -name '*.treefile' -print0 | parallel -0 Rscript ./pt.R {} | grep 'Unrooted' -B 7 | grep '\[1\]' | sed 's/\[1\] //' | sed 's/"//g' | parallel cat {} > all_trees.treefile

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

sup_trees: 
	find . -depth -maxdepth 1 -name '*_rep_seq.afa' -print0 |\
		parallel --progress -0\
		iqtree3 --redo -T AUTO -s {}

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
		iqtree3 --redo -T AUTO -s {}

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
			--min-seq-id 0.98 \
			--cov-mode 0\
			--alignment-mode 4\
			-v 1\
			--add-self-matches 1\
			--cluster-mode 1\
			-c 0.8

genomes:
	python3 ./download_genomes.py
