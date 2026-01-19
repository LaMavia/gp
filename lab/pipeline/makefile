all: genomes

clean:
	rm -rf ./sequences
	mkdir -p ./sequences
	touch ./sequences/.gitkeep

genomes:
	python3 ./download_sequences.py
