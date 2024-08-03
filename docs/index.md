# Introduction

## About `taxopy`

`taxopy` is a Python package that provides an interface to NCBI-formatted taxonomic databases. It enables various operations on taxonomic data, such as obtaining complete lineages, determining the lowest common ancestors (LCAs), retrieving taxa names from taxonomic identifiers, and more.

## Installation

You can install `taxopy` on your computer using Python's `pip` or through the [`conda`](https://conda.io/projects/conda/en/latest) or [`mamba`](https://mamba.readthedocs.io/en/latest) package managers:

=== "pip"

    ```sh
    pip install taxopy
    ```

=== "Conda"

    ```sh
    conda install -c conda-forge -c bioconda taxopy
    ```

=== "Mamba"

    ```sh
    mamba install -c conda-forge -c bioconda taxopy
    ```

!!! info "Enabling fuzzy search of taxon names"
    `taxopy` supports fuzzy string matching to [search for taxa with names that are similar but not identical to the queries][retrieval-of-taxa-with-nearly-matching-names-though-fuzzy-search]. This feature is not enabled by default to avoid additional dependencies. However, you can enable it by installing the `fuzzy-matching` extra using `pip`:

    ```sh
    pip install taxopy[fuzzy-matching]
    ```

    Alternatively, you can install the [`rapidfuzz`](https://rapidfuzz.github.io/RapidFuzz) library alongside `taxopy`:

    === "pip"

        ```sh
        pip install taxopy rapidfuzz
        ```

    === "Conda"

        ```sh
        conda install -c conda-forge -c bioconda taxopy rapidfuzz
        ```

    === "Mamba"

        ```sh
        mamba install -c conda-forge -c bioconda taxopy rapidfuzz
        ```

## Acknowledgements

Some of the code used to parse taxdump files in `taxopy` was adapted from [CAT/BAT](https://github.com/MGXlab/CAT_pack)[^1], a tool for taxonomic assignment of contigs and metagenome-assembled genomes.

[^1]: Von Meijenfeldt, F. A. B., Arkhipova, K., Cambuy, D. D., Coutinho, F. H. & Dutilh, B. E. "[Robust taxonomic classification of uncharted microbial sequences and bins with CAT and BAT](https://doi.org/10.1186/s13059-019-1817-x)". *Genome Biology* **20**, 217 (2019).