# taxopy

A Python package for obtaining complete lineages and the lowest common ancestor (LCA) from a set of taxonomic identifiers.

## Installation

There are two ways to install taxopy:

  - Using pip:

```
pip install taxopy
```

  - Using conda:

```
conda install -c conda-forge -c bioconda taxopy
```

## Usage

```python
import taxopy
```

First you need to download taxonomic information from NCBI's servers and put this data into a `TaxDb` object:


```python
taxdb = taxopy.TaxDb()
# You can also use your own set of taxonomy files:
taxdb = taxopy.TaxDb(nodes_dmp="taxdb/nodes.dmp", names_dmp="taxdb/names.dmp", keep_files=True)
```

The `TaxDb` object stores the name, rank and parent-child relationships of each taxonomic identifier:


```python
print(taxdb.taxid2name['2'])
print(taxdb.taxid2parent['2'])
print(taxdb.taxid2rank['2'])
```

    Bacteria
    131567
    superkingdom


To get information of a given taxon you can create a `Taxon` object using its taxonomic identifier:


```python
human = taxopy.Taxon('9606', taxdb)
gorilla = taxopy.Taxon('9593', taxdb)
lagomorpha = taxopy.Taxon('9975', taxdb)
```

Each `Taxon` object stores a variety of information, such as the rank, identifier and name of the input taxon, and the identifiers and names of all the parent taxa:


```python
print(lagomorpha.rank)
print(lagomorpha.name)
print(lagomorpha.name_lineage)
```

    order
    Lagomorpha
    ['Lagomorpha', 'Glires', 'Euarchontoglires', 'Boreoeutheria', 'Eutheria', 'Theria', 'Mammalia', 'Amniota', 'Tetrapoda', 'Dipnotetrapodomorpha', 'Sarcopterygii', 'Euteleostomi', 'Teleostomi', 'Gnathostomata', 'Vertebrata', 'Craniata', 'Chordata', 'Deuterostomia', 'Bilateria', 'Eumetazoa', 'Metazoa', 'Opisthokonta', 'Eukaryota', 'cellular organisms', 'root']


You can get the lowest common ancestor of a list of taxa using the `find_lca` function:


```python
human_lagomorpha_lca = taxopy.find_lca([human, lagomorpha], taxdb)
print(human_lagomorpha_lca.name)
```

    Euarchontoglires


You may also use the `find_majority_vote` to discover the most specific taxon that is shared by more than half of the lineages of a list of taxa:


```python
majority_vote = taxopy.find_majority_vote([human, gorilla, lagomorpha], taxdb)
print(majority_vote.name)
```

    Homininae

## Acknowledgements

Some of the code used in taxopy was taken from the [CAT/BAT tool for taxonomic classification of contigs and metagenome-assembled genomes](https://github.com/dutilh/CAT).