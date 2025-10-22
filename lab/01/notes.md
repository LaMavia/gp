doczytaj o GC-skew

ma genom kulisty

# technicznie:

1. pobrać
2. wziąć parametry z artykułu:
   - wielkość okna `w`
   - skok (ile przesuwamy się wsględem poprzedniej pozycji)
3. dla każdego okna liczymy GC-skew.
4. Ten ciąg rysujemy na diagramie

# wytłumaczenie:

zinterpretować ten diagram.

# Notatki

https://www.khanacademy.org/science/ap-biology/gene-expression-and-regulation/replication/a/molecular-mechanism-of-dna-replication

E. coli, like most bacteria, has a single origin of replication on its chromosome. The origin is about ‍245 base pairs long and has mostly A/T base pairs (which are held together by fewer hydrogen bonds than G/C base pairs), making the DNA strands easier to separate.

Żeby primerasa mogła dołączyć kolejny nukleotyd, ten obok musi mieć wolną grupę -OH (hydroksylową). Sam nukleotyd przychodzi jeszcze z grupą trójforforową (np. trójfosforan adeniny - ATP).

Strand dobudowujący się do strandu 5'-3' może łatwo dołączać nowe nukleotydy, bo polimerasa może działać tylko w kierunku 3'-5', bo może dodawać nukleotydy tylko od 3', bo ma ona wolną grupę hydroksylową.

Eukarioty mają jądro komórkowe, a prokarioty - nie. (też innych organelli).

https://en.wikipedia.org/wiki/Origin_of_replication

The necessity to regulate origin location likely arises from the need to coordinate DNA replication with other processes that act on the shared chromatin template to avoid DNA strand breaks and DNA damage.

Most bacterial chromosomes are circular and contain a single origin of chromosomal replication (oriC). Bacterial oriC regions are surprisingly diverse in size (ranging from 250 bp to 2 kbp), sequence, and organization.

## Z sugerowanego

https://nycdatascience.com/blog/student-works/using-the-gc-skew-to-analyze-bacterial-genome-evolution/

Nucleotide skews such as the GC skew can be used as a tool to identify the replication origin and terminus of the chromosome.

Due to the anti-parallel nature of DNA strands, the leading strand of the two replication forks copy opposing strands. This asymmetry, and the accompanying mutational footprint, appear to drive opposing GC skew values across replication terminus and origin sites.
