#import "@preview/codly:1.3.0": *
#import "@preview/codly-languages:0.1.1": *
#show: codly-init.with()

#import "@preview/grape-suite:3.1.0": exercise
#import exercise: project, task, subtask

#show: project.with(
    title: "Pipeline Filogenetyczny 2.0",

    university: [],
    institute: [],
    seminar: [],

    show-outline: true,

    author: "Zuzanna Surowiec 438730",

    show-solutions: false,
    date: datetime(day:04, month:02, year:2026)
)


#set table(
  stroke: none,
  gutter: 0.2em,
  fill: (x, y) =>
    if x == 0 or y == 0 { gray },
  inset: (right: 1.5em),
)

#show table.cell: it => {
  if it.x == 0 or it.y == 0 {
    set text(white)
    strong(it)
  } else if it.body == [] {
    // Replace empty cells with 'N/A'
    pad(..it.inset)[_N/A_]
  } else {
    it
  }
}

#let a = table.cell(
  fill: green.lighten(60%),
)[A]
#let b = table.cell(
  fill: aqua.lighten(60%),
)[B]

// "Wstęp", "Metody", "Wyniki", "Wnioski" z bibliografią na końcu

= Wstęp

Moją pracę oparłam na artykule badającym relacje pomiędzy rodzajami Brettanomyces, Debaryomyces, Dekkera oraz Kluyveromyces @base_publication. Wybrałam z niego 20 gatunków drożdży, starając się wybierać je w miarę proporcjonalnie do rozmiaru kladu, dbając jednocześnie o dostępność genomów w bazie NCBI. W powyrzszym artyluke, autorzy inferowali drzewo filegenetyczne, bazując na 18S rRNA  dla 116 genomów drożdży, z czego 28 z nich została zsekwencjonowana w ramach badania; pozostałe sekwencje pochodziły z baz GenBank oraz EMBL. Same drzewa zostały stworzone w oparciu o metodę NJ w narzędziu PHYLIP v3.5 po uliniowieniu sekwencji programem PILEUP i ręcznym dopasowaniu. Poziomy ufności zostały określone metodą bootstrap z 500 replikami.

Drzewo do porównania z literaturą napisałam ręcznie, pomijając wartości wsparcia. Do porównania użyłam również taksonomii NCBI @ncbi_taxonomy oraz Time Tree @timetree. 

= Metody 

// Metody powinny opisywać zastosowany pipeline z podsumowaniem narzędzi i innych skryptów, opis zastosowanych niestandardowych rozwiązań (np. filtracji, ukorzeniania itp.), opis zasobów komputerowych (jaki komputer, pamięć, czas działania).


1. W moim pipeline'ie bazowałam na proteomach z bazy NCBI @ncbi_genbank, pobranych przy użyciu narzędzia ncbi datasets @ncbi_datasets.
2. Tak pobrane proteomy poklastrowałam programem MMSeqs2 @mmseqs2, korzystając z klastrowania hierarchicznego, ponieważ dane nie były zbyt duże. Zmniejszyłam tu wartości parametrów `--min-seq-id 0.5` oraz `-c 0.7` w celu zwiększenia ilości klastrów ortologicznych.
3. Z obliczonych klastrów generowałam klastry ortologiczne. W tym celu skorzystałam z własnego skryptu w języku python (`make_orth.py`), działającego wielowątkowo z pomocą biblioteki tqdm @tqdm. Pomijałam tu klastry, które nie zawierały przynajmniej jednego reprezentanta dla każdego taksonu. W przypadku klastrów ortologicznych, zachłannie wybierałam sekwencje o długości najbliższej średniej długości sekwencji już wybranych, uporządkowanych w kolejności malejącej względem długości. W przypadku kilku sekwencji dla pierwszego taksonu w tej kolejności, wybierałam je losowo z rozkładu jednostajnego. Na tym etapie również zmieniałam etykiety sekwencji na nazwy taksonów.
4. Tak wygenerowane klastry uliniowiałam programem @muscle, korzystając z domyślnych opcji. Użyłam dodatkowo programu GNU parallel @gnu_parallel w celu przyspieszenia obliczeń, wykorzystując wszystkie rdzenie procesora. Programu tego używałam również na wielu innych etapach pipeline'u.
5. Na bazie uliniowionych klastrów, liczyłam drzewa metodą ML z programu IQ-TREE 3 @iqtree-3. W celach optymalizacyjnych, wybrałam najczęściej wybierane modele ewolucyjne na podstawie histogramu bazującego na najlepszych modelach dla pierwszych 50 drzew. W rezultacie, otrzymałam modele `LG+I+G4, Q.PFAM+I+G4, Q.PFAM+F+I+G4, Q.YEAST+I+G4, Q.YEAST+F+I+G4`. Zredukowało to ilość sprawdzanych modeli z $~1000$ do $~70$. W ramach punktu V.a, liczę tu również 1000 drzew bootstrap, korzystając z metody Ultrafast Bootstrap, gdyż metoda Bootstrap nie była obliczalna w sensownym czasie na moim komputerze.  
6. Drzewa zbudowane na klastrach ortologicznych filtrowałam na podstawie minimalnego wsparcia UFBoot/SH-aLRT na poziomie >30%, korzystając z IQ-TREE 3 oraz własnego skryptu w pythonie, sprawdzającego powyższy warunek (`filter_supported.py`). Przez filtr przeszło 202/241 drzew.
7. Na podstawie drzew ML dla klastrów ortologicznych oraz przefiltrowanych drzew ML dla klastrów ortologicznych, liczyłam drzewa konsensusowe metodą extended majority (domyślną).
8. Superdrzewa liczyłam na podstawie drzew ML dla klastrów ortologicznych. W tym celu, użyłam programu Clann @clann_main z kryterium dfit @clann_dfit, heurystyką wyszukiwania SPR, 20 krokami oraz 5 repetycjami.
9. Do porównania otrzymanych drzew użyłam biblioteki TreeDist @treedist_1 @treedist_2 @treedist_3 w R, korzystając z unormowanej odległości Robinsona-Fouldsa oraz unormowanej odległości Jaccarda-Robinsona-Fouldsa. Ze względu na brak wystarczających informacji o taksonach _Rhodotorula glutinis i Sporobolomyces roseus_ w bazie TimeTree, musiałam je usunąć z drzew wynikowych. W tym celu użyłam pakietu biopython @biopython, dokładnie metody `Bio.Phylo.Newick.Tree.prune(<missing_taxon>)` oraz usunęłam długości krawędzi z obydwu drzew poleceniem `sed`, gdyż zostały one wyzerowane po operacji `prune`, co dawało brzydki wykres porównania.

Do samej organizacji zadań użyłam programu GNU Make, który wymaga ustawienia zmiennej środowiskowej `NCBI_API_KEY`. Do uruchomienia pipeline'u powinno wystarczyć wykonanie polecenia `make`. Przy urównoleglaniu pipeline'u zdecydowałam się na uliniowianie warstwowe, tj. w obrębie jednego zadania, z użyciem GNU Parallel, gdyż wykonujemy serię bardzo podobnych poleceń, które czasami wymagają wszystkich wyników z poprzedniego zadania (np. liczenie drzew konsensusowych wymaga policzenia wszystkich drzew ML dla klastrów ortologicznych). Skrypt ten nie jest zatem przystosowany do uruchamiania go z parametrem `-j n` dla $n > 1$.

= Wyniki

== Środowisko

Pipeline został uruchomiony na moim komputerze z procesorem AMD Ryzen 7 5700U (16) \@ 4.3GHz, 
30.69 GiB dostępnej pamięci RAM DDR4, na systemie NixOS 26.05 z kernelem 6.18.0-zen1.

Długość całych obliczeń trwała ok. 2.5h, z czego liczenie drzew ML zajęło ok. 1.5h.

== Rozkład klastrów 

#figure( 
  image("./cluster_sizes.svg"),
  caption:[Rozkład rozmiaru wszystkich klastrów w skali logarytmicznej. Pierwszy kubełek odpowiada klastrom, które na pewno zostały odrzucone. Najmniejszy klaster miał wielkość 2, a największy — 248.]
) <cluster_sizes>

== Porównania

#figure(
  image("./scores.svg"),
  caption: [Porównania różnych metod inferencji z różnymi referencjami]
)

#figure(
  table(
    columns: 4,
    [method],   [reference],      [nRF],     [nJRF],
    [Orth. Con.],[NCBI], [0.333333], [0.296296],
    [Orth. Con.], [Publication], [0.235294], [0.106209],
    [Orth. Con.],[Time Tree],[0.066667],[0.040000],
    [Orth. Filtered Con.],[NCBI],[0.333333],[0.296296],
    [Orth. Filtered Con.],[Publication],[0.235294],[0.106209],
    [Orth. Filtered Con.],[Time Tree],[0.066667],[0.040000],
    [Orth. Super],[NCBI],[0.333333],[0.296296],
    [Orth. Super],[Publication],[0.235294],[0.116013],
    [Orth. Super],[Time Tree],[0.066667],[0.040000]
  ),
  caption: [Tabela porównań uzyskanych drzew z drzewami referencyjnymi.]
)

=== Wizualizacje TreeDist

==== Drzewo konsensusowe, klastry ortologiczne i filtrowane

#figure(
  grid(
    columns: 2,
    rows: 3,
    image("./oc-ncbi.jpg"), image("./foc-ncbi.jpg"),
    image("./oc-pub.jpg"), image("./foc-pub.jpg"),
    image("./oc-tt.jpg"), image("./foc-tt.jpg")
  ),
  caption: [Porównania drzew konsensusowych z klastrów ortologicznych (lewo) i drzew konsensusowych z przefiltrowanych drzew na klastrach ortologicznych (prawo) z drzewami referencyjnymi, używając miary nJRF.]
)

==== Super drzewo

#figure(
  block(
    grid(
      columns: 3,
      rows: 1,
      image("./st-ncbi.jpg"),
      image("./st-pub.jpg"),
      image("./st-tt.jpg")
    ),
    width: 130%,
    outset: (x: 50pt),
    sticky: true
  ),
  caption: [Porównanie super drzewa z drzew ML na klastrach ortologicznych z drzewami referencyjnymi, używając miary nJRF.]
)

= Wnioski

== Podsumowanie

Wyniki przejawiają bardzo wysokie podobieństwo do drzewa z bazy TimeTree, które wydaje się być tu preferowane ze względu na ograniczony zbiór danych w oryginalnej publikacji oraz wątpliwą jakość taksonomii NCBI (w tym przypadku).

== Uwagi

=== Ograniczenia modeli

Warte może być zezwolenie na wybór modelu z większej puli modeli podczas liczenia drzew ML z IQ-TREE. Tak silne ograniczenie wyboru modelu jak tutaj może prowadzić do mniej reprezentatywnych drzew ML, wpływając w znacznym stopniu na jakość wyników końcowych. 

Samo ograniczenie zostało wybrane tu w celu optymalizacji czasu działania pipeline'u, gdyż Model Finder zajmował znaczną część czasu liczenia drzew ML.

=== Bootstrap 

Ponownie ze względów optymalizacyjnych, został tu użyty Ultrafast Bootstrap zamiast nieparametrycznego Bootstrapu. Również mogło wpłynąć to na jakość wyników, ponieważ UFBoot używa zaledwie przybliżenia MLE.

Jednakże, użycie zwykłego bootstrapu prowadziłoby tu do ok. 100-1000x wydłużenia czasu działania pipeline'u (w zależności od liczby powtórzeń), co nie było tu praktyczne.

=== Ponowne klastrowanie

Jak widać na rozkładzie wielkości klastrów @cluster_sizes, powalająca większość klastrów zostala odrzucona przy generowaniu klastrów ortologicznych ze względy na brak reprezentantów dla każdego taksonu. Jednym z potencjalnych rozwiązań byłoby tu ponowne poklastrowanie takich klastrów, używając luźniejszych kryteriów klastrowania, np. zmniejszając wartości parametrów `-c` oraz `--min-seq-id`. Taka operacja mogłaby zostać powtórzona kilkukrotnie.

Sama korzyść płynąca z dodania nowych, mniej konserwatywnych klastrów pozostaje do zbadania.


#bibliography("gp-pipeline-2.bib", title: "Bibliografia")
