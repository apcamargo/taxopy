# taxopy

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6993581.svg)](https://doi.org/10.5281/zenodo.6993581)

A Python package for manipulating NCBI-formatted taxonomic databases. Allows you to obtain complete lineages, determine lowest common ancestors (LCAs), get taxa names from their taxids, and more!

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

> [!NOTE]
> To enable fuzzy matching of taxonomic names, you need to install the `fuzzy-matching` extra. This can be done by adding `[fuzzy-matching]` to the installation command in pip:
> ```
> pip install taxopy[fuzzy-matching]
> ```
> Alternatively, you can install the `rapidfuzz` library:
> ```
> # Using pip
> pip install rapidfuzz
> # Using conda
> conda install -c conda-forge rapidfuzz
> ```

## Usage

```python
import taxopy
```

First you need to download taxonomic information from NCBI's servers and put this data into a `TaxDb` object:

```python
taxdb = taxopy.TaxDb()
# You can also use your own set of taxonomy files:
taxdb = taxopy.TaxDb(nodes_dmp="taxdb/nodes.dmp", names_dmp="taxdb/names.dmp")
# If you want to support legacy taxonomic identifiers (that were merged to other identifier), you also need to provide a `merged.dmp` file. This is not necessary if the data is being downloaded from NCBI.
taxdb = taxopy.TaxDb(nodes_dmp="taxdb/nodes.dmp", names_dmp="taxdb/names.dmp", merged_dmp="taxdb/merged.dmp")
```

The `TaxDb` object stores the name, rank and parent-child relationships of each taxonomic identifier:

```python
print(taxdb.taxid2name[2])
print(taxdb.taxid2parent[2])
print(taxdb.taxid2rank[2])
```

    Bacteria
    131567
    superkingdom

If you want to retrieve the new taxonomic identifier of a legacy identifier you can use the `oldtaxid2newtaxid` attribute:

```python
print(taxdb.oldtaxid2newtaxid[260])
```

    143224

To get information of a given taxon you can create a `Taxon` object using its taxonomic identifier:

```python
saccharomyces = taxopy.Taxon(4930, taxdb)
human = taxopy.Taxon(9606, taxdb)
gorilla = taxopy.Taxon(9593, taxdb)
lagomorpha = taxopy.Taxon(9975, taxdb)
```

Each `Taxon` object stores a variety of information, such as the rank, identifier and name of the input taxon, and the identifiers and names of all the parent taxa:

```python
print(lagomorpha.rank)
print(lagomorpha.name)
print(lagomorpha.name_lineage)
print(lagomorpha.ranked_name_lineage)
print(lagomorpha.rank_name_dictionary)
```

    order
    Lagomorpha
    ['Lagomorpha', 'Glires', 'Euarchontoglires', 'Boreoeutheria', 'Eutheria', 'Theria', 'Mammalia', 'Amniota', 'Tetrapoda', 'Dipnotetrapodomorpha', 'Sarcopterygii', 'Euteleostomi', 'Teleostomi', 'Gnathostomata', 'Vertebrata', 'Craniata', 'Chordata', 'Deuterostomia', 'Bilateria', 'Eumetazoa', 'Metazoa', 'Opisthokonta', 'Eukaryota', 'cellular organisms', 'root']
    [('order', 'Lagomorpha'), ('clade', 'Glires'), ('superorder', 'Euarchontoglires'), ('clade', 'Boreoeutheria'), ('clade', 'Eutheria'), ('clade', 'Theria'), ('class', 'Mammalia'), ('clade', 'Amniota'), ('clade', 'Tetrapoda'), ('clade', 'Dipnotetrapodomorpha'), ('superclass', 'Sarcopterygii'), ('clade', 'Euteleostomi'), ('clade', 'Teleostomi'), ('clade', 'Gnathostomata'), ('clade', 'Vertebrata'), ('subphylum', 'Craniata'), ('phylum', 'Chordata'), ('clade', 'Deuterostomia'), ('clade', 'Bilateria'), ('clade', 'Eumetazoa'), ('kingdom', 'Metazoa'), ('clade', 'Opisthokonta'), ('superkingdom', 'Eukaryota'), ('no rank', 'cellular organisms'), ('no rank', 'root')]
    {'order': 'Lagomorpha', 'clade': 'Opisthokonta', 'superorder': 'Euarchontoglires', 'class': 'Mammalia', 'superclass': 'Sarcopterygii', 'subphylum': 'Craniata', 'phylum': 'Chordata', 'kingdom': 'Metazoa', 'superkingdom': 'Eukaryota'}

You can use the `parent` method to get a `Taxon` object of the parent node of a given taxon:

```python
lagomorpha_parent = lagomorpha.parent(taxdb)
print(lagomorpha_parent.rank)
print(lagomorpha_parent.name)
```

    clade
    Glires

### LCA and majority vote

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

The `find_majority_vote` function allows you to control its stringency via the `fraction` parameter. For instance, if you would set `fraction` to 0.75 the resulting taxon would be shared by more than 75% of the input lineages. By default, `fraction` is 0.5.

```python
majority_vote = taxopy.find_majority_vote([human, gorilla, lagomorpha], taxdb, fraction=0.75)
print(majority_vote.name)
```

    Euarchontoglires

You can also assign weights to each input lineage:

```python
majority_vote = taxopy.find_majority_vote([saccharomyces, human, gorilla, lagomorpha], taxdb)
weighted_majority_vote = taxopy.find_majority_vote([saccharomyces, human, gorilla, lagomorpha], taxdb, weights=[3, 1, 1, 1])
print(majority_vote.name)
print(weighted_majority_vote.name)
```

    Euarchontoglires
    Opisthokonta

To check the level of agreement between the taxa that were aggregated using `find_majority_vote` and the output taxon, you can check the `agreement` attribute.

```python
print(majority_vote.agreement)
print(weighted_majority_vote.agreement)
```

    0.75
    1.0

### Taxid from name

If you only have the name of a taxon, you can get its corresponding taxid using the `taxid_from_name` function:

```python
taxid = taxopy.taxid_from_name('Homininae', taxdb)
print(taxid)
```

    [207598]

This function returns a list of all taxonomic identifiers associated with the input name. In the case of homonyms, the list will contain multiple taxonomic identifiers:

```python
taxid = taxopy.taxid_from_name('Aotus', taxdb)
print(taxid)
```

    [9504, 114498]

In case a list of names is provided as input, the function will return a list of lists.

```python
taxid = taxopy.taxid_from_name(['Homininae', 'Aotus'], taxdb)
print(taxid)
```

    [[207598], [9504, 114498]]

In certain situations, it is useful to allow slight variations between the input name and the matches in the database. This can be accomplished by setting the `fuzzy` parameter of `taxid_from_name` to `True`. For instance, in GTDB, some taxa have suffixes. The `fuzzy` parameter enables you to locate the taxonomic identifiers of all taxa with a name similar to the input, so you don't need to know the exact name beforehand.

```python
# The `taxdump_url` parameter of the `TaxDb` class can be used retrieve a custom taxdump from a URL. In this case, we will use a GTDB taxdump provided by Wei Shen (https://github.com/shenwei356/gtdb-taxdump)
gtdb_taxdb = taxopy.TaxDb(taxdump_url="https://github.com/shenwei356/gtdb-taxdump/releases/download/v0.5.0/gtdb-taxdump-R220.tar.gz")
for t in taxopy.taxid_from_name("Myxococcota", gtdb_taxdb, fuzzy=True):
    print(taxopy.Taxon(t, gtdb_taxdb).name)
```

    Myxococcota_A
    Myxococcota

You can control the minimum similarity between the input name and the matches in the database by setting the `score_cutoff` parameter (default is 0.9).

```python
for t in taxopy.taxid_from_name(
    "Myxococcota", gtdb_taxdb, fuzzy=True, score_cutoff=0.7
):
    print(taxopy.Taxon(t, gtdb_taxdb).name)
```

    Myxococcales
    Myxococcota_A
    Myxococcus
    Myxococcia
    Myxococcota
    Myxococcaceae

## Acknowledgements

Some of the code used in taxopy was taken from the [CAT/BAT tool for taxonomic classification of contigs and metagenome-assembled genomes](https://github.com/dutilh/CAT).
