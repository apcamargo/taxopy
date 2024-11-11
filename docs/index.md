# Introduction

## About `taxopy`

`taxopy` is a Python package that provides an interface for assessing NCBI-formatted taxonomic databases. It enables various operations on taxonomic data, such as obtaining complete lineages, determining the lowest common ancestors (LCAs), retrieving taxa names from taxonomic identifiers, and more.

## Installation

You can install `taxopy` on your computer using Python's `pip`, [`uv`](https://docs.astral.sh/uv/), or through the [`pixi`](https://pixi.sh/latest/), [`conda`](https://conda.io/projects/conda/en/latest) or [`mamba`](https://mamba.readthedocs.io/en/latest) package managers:

=== "pip"

    ```shell-session
    $ pip install taxopy
    ```

=== "uv"

    ```shell-session
    $ uv init example
    $ cd example
    $ uv add taxopy
    ```

=== "Pixi"

    ```shell-session
    $ pixi init --channel conda-forge --channel bioconda example
    $ cd example
    $ pixi add taxopy
    ```

=== "Conda"

    ```shell-session
    $ conda create -n taxopy-env -c conda-forge -c bioconda taxopy
    $ conda activate taxopy-env
    ```

=== "Mamba"

    ```shell-session
    $ mamba create -n taxopy-env -c conda-forge -c bioconda taxopy
    $ mamba activate taxopy-env
    ```

!!! info "Enabling fuzzy search of taxon names"
    `taxopy` supports fuzzy string matching to [search for taxa with names that are similar but not identical to the queries][retrieval-of-taxa-with-nearly-matching-names-though-fuzzy-search]. This feature is not enabled by default to avoid additional dependencies. However, you can enable it by installing the `fuzzy-matching` extra using `pip` or `uv`:

    === "pip"

        ```shell-session
        $ pip install taxopy[fuzzy-matching]
        ```

    === "uv"

        ```shell-session
        $ uv init example
        $ cd example
        $ uv add taxopy --extra fuzzy-matching
        ```

    Alternatively, you can install the [`rapidfuzz`](https://rapidfuzz.github.io/RapidFuzz) library alongside `taxopy`:

    === "pip"

        ```shell-session
        $ pip install taxopy rapidfuzz
        ```

    === "uv"

        ```shell-session
        $ uv init example
        $ cd example
        $ uv add taxopy rapidfuzz
        ```

    === "Pixi"

        ```shell-session
        $ pixi init --channel conda-forge --channel bioconda example
        $ cd example
        $ pixi add taxopy rapidfuzz
        ```

    === "Conda"

        ```shell-session
        $ conda create -n taxopy-env -c conda-forge -c bioconda taxopy rapidfuzz
        $ conda activate taxopy-env
        ```

    === "Mamba"

        ```shell-session
        $ mamba create -n taxopy-env -c conda-forge -c bioconda taxopy rapidfuzz
        $ mamba activate taxopy-env
        ```

## Acknowledgements

Some of the code used to parse taxdump files in `taxopy` was adapted from [CAT/BAT](https://github.com/MGXlab/CAT_pack)[^1], a tool for taxonomic assignment of contigs and metagenome-assembled genomes.

[^1]: Von Meijenfeldt, F. A. B., Arkhipova, K., Cambuy, D. D., Coutinho, F. H. & Dutilh, B. E. "[Robust taxonomic classification of uncharted microbial sequences and bins with CAT and BAT](https://doi.org/10.1186/s13059-019-1817-x)". *Genome Biology* **20**, 217 (2019).
