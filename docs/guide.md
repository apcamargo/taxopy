# Guide

## Initializing a taxonomy database in a `TaxDb` object

To get started, you need to create a [`TaxDb`][taxopy.TaxDb] object, which will store data related to the taxonomic database, such as taxonomic identifiers (or TaxIds), names, and hierarchies. This can be achieved by downloading the set of files that store this data, known as [taxdump](https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump_readme.txt), from an online source (NCBI by default) or by providing your own taxdump files.

=== "Downloading from NCBI"

    ```python
    >>> import taxopy
    >>> taxdb = taxopy.TaxDb()# (1)!
    ```

    1. By default, `taxopy` deletes the taxdump files after creating the object. To retain the files in the working directory, set `keep_files=True`. You can specify the directory where the files are stored using the `taxdb_dir` parameter.

=== "Downloading from a different source"

    ```python
    >>> import taxopy
    >>> url = "https://github.com/shenwei356/gtdb-taxdump/releases/download/v0.5.0/gtdb-taxdump-R220.tar.gz"
    >>> taxdb = taxopy.TaxDb(
    ...     taxdump_url=url# (1)!
    ... )
    ```

    1. The `taxdump_url` parameter is used to specify the URL of the taxdump file to download. In this case, we are using a [custom a GTDB taxdump provided by Wei Shen](https://github.com/shenwei356/gtdb-taxdump).

=== "Local taxdump"

    ```python
    >>> import taxopy
    >>> taxdb = taxopy.TaxDb(
    ...     nodes_dmp="taxdb/nodes.dmp",
    ...     names_dmp="taxdb/names.dmp",
    ...     merged_dmp="taxdb/merged.dmp",# (1)!
    ... )
    ```

    1. The `merged_dmp` parameter is optional. However, if you want to support legacy TaxIds (those merged into other identifiers), you need to provide a `merged.dmp` file. This is not necessary if the data is downloaded from an online source, which will include its own merged.dmp file.

The [`TaxDb`][taxopy.TaxDb] object stores the names, ranks, and parent-child relationships of all taxa, each represented by their respective TaxIds. For instance, [TaxId 2](https://www.ncbi.nlm.nih.gov/datasets/taxonomy/2/) corresponds to the "*Bacteria*" taxon, which has the rank of superkingdom. The parent taxon of *Bacteria* is [TaxId 131567](https://www.ncbi.nlm.nih.gov/datasets/taxonomy/131567/), corresponding to "*cellular organisms*".

```python
>>> print(taxdb.taxid2name[2])
Bacteria
>>> print(taxdb.taxid2rank[2])
superkingdom
>>> print(taxdb.taxid2parent[2])
131567
```

To retrieve the TaxId to which a legacy TaxId has been merged, you can use the `merged2newtaxid` attribute. For instance, the legacy TaxIds 260 and 29537 have been merged into [TaxId 143224](https://www.ncbi.nlm.nih.gov/datasets/taxonomy/143224/) (*Zobellia uliginosa*).

```python
>>> print(taxdb.oldtaxid2newtaxid[260])
143224
>>> print(taxdb.oldtaxid2newtaxid[29537])
143224
```

## The `Taxon` object

[`Taxon`][taxopy.Taxon] objects represent individual taxa within the taxonomy database. These objects are initialized using a TaxId and a corresponding [`TaxDb`][taxopy.TaxDb] object, from which the taxon data is retrieved.

```python
>>> saccharomyces = taxopy.Taxon(4930, taxdb)
>>> human = taxopy.Taxon(9606, taxdb)
>>> gorilla = taxopy.Taxon(9593, taxdb)
>>> lagomorpha = taxopy.Taxon(9975, taxdb)
```

Each [`Taxon`][taxopy.Taxon] object stores various data related to the taxon, including its TaxId, name, rank, and lineage. The lineage data comprises the TaxIds, names, and ranks of its parent taxa.

```python
>>> print(lagomorpha.rank)
order
>>> print(lagomorpha.name)
Lagomorpha
>>> print(lagomorpha.name_lineage)
['Lagomorpha', 'Glires', 'Euarchontoglires', 'Boreoeutheria', 'Eutheria', 'Theria', 'Mammalia', 'Amniota', 'Tetrapoda', 'Dipnotetrapodomorpha', 'Sarcopterygii', 'Euteleostomi', 'Teleostomi', 'Gnathostomata', 'Vertebrata', 'Craniata', 'Chordata', 'Deuterostomia', 'Bilateria', 'Eumetazoa', 'Metazoa', 'Opisthokonta', 'Eukaryota', 'cellular organisms', 'root']
>>> print(lagomorpha.ranked_name_lineage)
[('order', 'Lagomorpha'), ('clade', 'Glires'), ('superorder', 'Euarchontoglires'), ('clade', 'Boreoeutheria'), ('clade', 'Eutheria'), ('clade', 'Theria'), ('class', 'Mammalia'), ('clade', 'Amniota'), ('clade', 'Tetrapoda'), ('clade', 'Dipnotetrapodomorpha'), ('superclass', 'Sarcopterygii'), ('clade', 'Euteleostomi'), ('clade', 'Teleostomi'), ('clade', 'Gnathostomata'), ('clade', 'Vertebrata'), ('subphylum', 'Craniata'), ('phylum', 'Chordata'), ('clade', 'Deuterostomia'), ('clade', 'Bilateria'), ('clade', 'Eumetazoa'), ('kingdom', 'Metazoa'), ('clade', 'Opisthokonta'), ('superkingdom', 'Eukaryota'), ('no rank', 'cellular organisms'), ('no rank', 'root')]
>>> print(lagomorpha.rank_name_dictionary)
OrderedDict({'order': 'Lagomorpha', 'clade': 'Opisthokonta', 'superorder': 'Euarchontoglires', 'class': 'Mammalia', 'superclass': 'Sarcopterygii', 'subphylum': 'Craniata', 'phylum': 'Chordata', 'kingdom': 'Metazoa', 'superkingdom': 'Eukaryota'})
```

To obtain the [`Taxon`][taxopy.Taxon] object for the parent of a specified taxon, you can use the `parent` method.

```python
>>> lagomorpha_parent = lagomorpha.parent(taxdb)
>>> print(lagomorpha_parent.name)
Glires
>>> print(lagomorpha_parent.rank)
clade
```

## Retrieval of taxa with nearly matching names though fuzzy search

When querying a [`TaxDb`][taxopy.TaxDb] using a taxon name, you can enable fuzzy search by setting the `fuzzy` parameter of [`taxid_from_name`][taxopy.taxid_from_name] to `True`. This allows the function to find taxa with names similar, but not identical, to the query string(s).

For a practical use case of this feature, consider the [GTDB](https://gtdb.ecogenomic.org/) taxonomy. In GTDB [some taxa have suffixes appended to their names](https://gtdb.ecogenomic.org/faq#why-do-some-family-and-higher-rank-names-end-with-an-alphabetic-suffix) because they are either not monophyletic in the GTDB reference tree or have unstable placements between different releases. By using fuzzy searches, you can find all the TaxIds representing a given taxon, such as *Myxococcota*, without needing to know in advance if any suffixes are appended to the name.

```python
>>> url = "https://github.com/shenwei356/gtdb-taxdump/releases/download/v0.5.0/gtdb-taxdump-R220.tar.gz"
>>> gtdb_taxdb = taxopy.TaxDb(taxdump_url=url)# (1)!
>>> for t in taxopy.taxid_from_name("Myxococcota", gtdb_taxdb, fuzzy=True):
...     print(taxopy.Taxon(t, gtdb_taxdb).name)
Myxococcota_A
Myxococcota
```

1. This custom GTDB taxdump was generated by Wei Shen using the [TaxonKit](https://bioinf.shenwei.me/taxonkit/) toolkit and is available for download from [GitHub](https://github.com/shenwei356/gtdb-taxdump).

You can adjust the minimum similarity threshold between the query string(s) and the matches in the database using the `score_cutoff` parameter, which determines how closely a name must match a query string to be considered a valid result. The default value is `0.9`, but you can lower this threshold to find matches that are less similar to the queries.

```python
>>> for t in taxopy.taxid_from_name(
...     "Myxococcota", gtdb_taxdb, fuzzy=True, score_cutoff=0.7
... ):
...     print(taxopy.Taxon(t, gtdb_taxdb).name)
Myxococcales
Myxococcota_A
Myxococcus
Myxococcia
Myxococcota
Myxococcaceae
```
