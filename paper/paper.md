---
title: "`Taxopy`: A Python package for obtaining complete lineages and the lowest common ancestor (LCA) from a set of taxonomic identifiers"
tags:
  - python
  - biology
  - evolution
  - bioinformatics

authors:
  - name: Antonio Pedro Camargo
    orcid: 0000-0003-3913-2484
    affiliation: "1, 2"
    corresponding: true
  - name: Mateus B. Fiamenghi
    orcid: 0000-0003-4535-8594
    affiliation: 1
    corresponding: true
affiliations:
  - name: DOE Joint Genome Institute, Lawrence Berkeley National Laboratory, Berkeley, United States
    index: 1
  - name: Department of Biochemistry, Institute of Chemistry, University of São Paulo, São Paulo, Brazil
    index: 2
date: 26 February 2026
bibliography: paper.bib
---

# Summary

Dobzhansky once famously said, "Nothing in biology makes sense except in the light of evolution" [@dobzhansky1964]. Indeed, without an evolutionary perspective, hypothesis testing of biological systems would be severely limited to simple data analysis. This is especially true in the age of big data, where large datasets of genomic, transcriptomic, and proteomic information are being generated at an unprecedented rate.

`Taxopy` is a Python package that provides an accessible programmatic interface for navigating these complex evolutionary relationships. It allows researchers to seamlessly convert basic taxonomic identifiers into complete evolutionary lineages, find the lowest common ancestor (LCA) among groups of organisms, and translate between different taxonomic databases. By handling the heavy lifting of taxonomic data parsing, `Taxopy` enables biologists and bioinformaticians to easily integrate evolutionary context into their data analysis workflows.

# Statement of need

Obtaining complete lineages and the lowest common ancestor (LCA) from a set of taxonomic identifiers has historically been a complex task, especially when dealing with large datasets. Furthermore, differing standards for taxonomic classification, such as the National Center for Biotechnology Information (NCBI) taxonomy [@schoch2020] and the Genome Taxonomy Database GTDB [@parks2025] for prokaryotes, often lead to inconsistencies and difficulties in data integration.

To map taxonomic lineages to numeric identifiers and compute relationships between organisms, several bioinformatics tools utilize "taxdumps", a file format pioneered by NCBI. However, parsing and utilizing these taxdump files outside of specialized programs is non-trivial.

`Taxopy` is a python package designed to simplify the retrieval of taxonomic ranks and lineages for researchers from any biological field, by allowing users to obtain complete lineages by mapping numeric identifiers or taxa names directly against taxdump files. Furthermore, the package contains helper functions to retrieve the LCA from a list of taxonomic identifiers, as well as to compute a majority-vote consensus when comparing taxa where a subset is more distantly related. `Taxopy` is particularly useful for researchers working with large datasets, as it streamlines taxonomic classification and facilitates comparative evolutionary analyses.

# State of the field

Several tools currently exist to facilitate taxonomic data manipulation, such as the `ETE toolkit` [@huerta-cepas2016], [`taxize`](https://github.com/ropensci/taxize) and `Taxonkit` [@shen2021]. Below we list the main attributes of each of these programs:

- `ETE toolkit`: a python package mostly tailored for manipulating phylogenies and hypothesis testing via CodeML [@yang2002] and Slr [@massingham2005], but also includes some taxonomy parsing helpers.

- `taxize`: an R package that maps taxonomic data via web APIs across many sources, and does not rely on taxdump files.

- `Taxonkit`: a CLI tool designed for high-throughput shell manipulation of taxonomic data, capable of creating novel taxdump files.

While these tools offer overlapping functionalities, such as programmatic access to hierarchical taxonomy operations, identifier resolution, and LCA computation, `Taxopy` is uniquely positioned in the ecosystem. First, it is designed to be integrated into custom python workflows, or used as a lightweight dependency for other python libraries leveraging its low-level functions. Second, `Taxopy` provides specialized functions to calculate the majority vote between distantly related taxa when a LCA would be too broad, and handle inconsistencies between different taxonomic database by converting names between different taxdumps.

# Software design

The core design of `Taxopy` is around the `Taxon` object, from which all taxonomic attributes stem. To initialize a `Taxon`, a taxdump file is required. `Taxopy` enables users to easily download or pass a taxdump through the flexible `TaxDb` object, which then eagerly parses the taxdump into python dictionaries to allow for rapid, in-memory searches.

Once a `Taxon` object is initialized, users can explore different lineage attributes, including the hierarchical organization (which allows retrieving the parent lineage), alternative taxa names, and the full lineage (including sublineages). The API provides users the flexibility to format the returned objects as needed; for instance, leveraging the `Taxon.rank_name_dictionary` method to generate a Greengenes-formatted string [@mcdonald2023], a standard widely used for taxonomic representation in microbiome research.

To ensure broad compatibility and minimize dependencies, `Taxopy` is designed as a mostly pure-Python package. It relies only on `flit_core` for PyPI deployment, `pytest` for testing, and the optional `rapidfuzz` dependency to enable fuzzy searching of partial name matches via the `taxid_from_name` utility function. Consequently, the internal objects are implemented using native Python dictionaries and standard library data structures, ensuring a lightweight footprint and fast execution times.

# Research impact statement

`Taxopy` has seen positive reception and adoption within the scientific community. Since its release, the package has accrued over 59 thousand downloads on Bioconda, has more than 50 GitHub stars, and generated several forks, demonstrating its active use in the open-source ecosystem. Furthermore, it has been cited in several peer-reviewed publications [@camargo2023; @fiamenghi2025; @fiamenghi2025a; @shen2021a], confirming its utility in active research.

# AI usage disclosure

Generative AI (Codex) was used to aid in writing comprehensive unit tests for the software; all generated code was manually reviewed and revised by the authors for soundness. Google Gemini was used for grammar correction and structural editing of this manuscript.

# Acknowledgements

A.P.C wrote the software and revised the manuscript

M.B.F revised the software and wrote the manuscript

# References
