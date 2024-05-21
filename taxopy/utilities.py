# -*- coding: utf-8 -*-
#
#   This file is part of the taxopy package, available at:
#   https://github.com/apcamargo/taxopy
#
#   Taxopy is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see <https://www.gnu.org/licenses/>.
#
#   Contact: antoniop.camargo@gmail.com

import importlib
import types
import warnings
from collections import Counter, defaultdict
from itertools import zip_longest
from typing import List, Optional, Union

from taxopy.core import TaxDb, Taxon, _AggregatedTaxon
from taxopy.exceptions import LCAError, MajorityVoteError


def _import_optional_dependency(name: str) -> types.ModuleType:
    """
    Import an optional dependency.

    Parameters
    ----------
    name : str
        The module name.

    Returns
    -------
    maybe_module : types.ModuleType
        The imported module.
    """

    msg = f"Missing optional dependency '{name}'. Use pip or conda to install {name}."
    try:
        module = importlib.import_module(name)
    except ImportError as err:
        raise ImportError(msg) from err
    return module


def _get_taxid_from_multiple_names(names, taxdb, fuzzy, score_cutoff):
    name2taxid = defaultdict(list)
    for taxid, taxname in taxdb.taxid2name.items():
        if not taxdb._merged_dmp or taxid not in taxdb.oldtaxid2newtaxid:
            name2taxid[taxname].append(taxid)
    if fuzzy:
        rapidfuzz = _import_optional_dependency("rapidfuzz")
        taxid_list = [
            [
                taxid
                for match, _, _ in rapidfuzz.process.extract(
                    name,
                    name2taxid.keys(),
                    scorer=rapidfuzz.fuzz.ratio,
                    processor=rapidfuzz.utils.default_process,
                    score_cutoff=score_cutoff,
                    limit=None,
                )
                for taxid in name2taxid[match]
            ]
            for name in names
        ]
    else:
        taxid_list = [name2taxid[name] for name in names]
    return taxid_list


def _get_taxid_from_single_name(name, taxdb, fuzzy, score_cutoff):
    if fuzzy:
        rapidfuzz = _import_optional_dependency("rapidfuzz")
        matches = {
            match
            for match, _, _ in rapidfuzz.process.extract(
                name,
                taxdb.taxid2name.values(),
                scorer=rapidfuzz.fuzz.ratio,
                processor=rapidfuzz.utils.default_process,
                score_cutoff=score_cutoff,
                limit=None,
            )
        }
        taxid_list = [
            taxid for taxid, taxname in taxdb.taxid2name.items() if taxname in matches
        ]
    else:
        taxid_list = [
            taxid for taxid, taxname in taxdb.taxid2name.items() if taxname == name
        ]
    if taxdb._merged_dmp:
        taxid_list = [
            taxid for taxid in taxid_list if taxid not in taxdb.oldtaxid2newtaxid
        ]
    return taxid_list


def taxid_from_name(
    names: Union[str, List[str]],
    taxdb: TaxDb,
    fuzzy: bool = False,
    score_cutoff: float = 0.9,
) -> Union[List[int], List[List[int]]]:
    """
    Takes one (or more) taxon name and returns a list (or list of lists)
    containing the taxonomic identifiers associated with it (or them).

    Parameters
    ----------
    name : str or list of str
        The name of the taxon whose taxonomic identifier will be returned. A
        list of names can also be provided.
    taxdb : TaxDb
        A TaxDb object.
    fuzzy : bool, default False
        If True, the input name will be matched to the taxa names in the
        database using fuzzy string matching.
    score_cutoff : float, default 0.9
        The minimum score required for a match to be considered valid when
        fuzzy string matching is used. This value must be between 0.0 and 1.0.

    Returns
    -------
    list or list of list
        A list of all the taxonomic identifiers associated with the input taxon
        name. If a list of names is provided, a list of lists is returned.
    """
    score_cutoff = score_cutoff * 100
    if isinstance(names, list):
        taxid_list = _get_taxid_from_multiple_names(names, taxdb, fuzzy, score_cutoff)
        if not all(len(taxids) for taxids in taxid_list):
            warnings.warn(
                "At least one of the input names was not found in the taxonomy database.",
                Warning,
            )
    else:
        taxid_list = _get_taxid_from_single_name(names, taxdb, fuzzy, score_cutoff)
        if not len(taxid_list):
            warnings.warn(
                "The input name was not found in the taxonomy database.", Warning
            )
    return taxid_list


def find_lca(taxon_list: List[Taxon], taxdb: TaxDb) -> Taxon:
    """
    Takes a list of multiple Taxon objects and returns their lowest common
    ancestor (LCA).

    Parameters
    ----------
    taxon_list : list
        A list containing at least two Taxon objects.
    taxdb : TaxDb
        A TaxDb object.

    Returns
    -------
    _AggregatedTaxon
        The _AggregatedTaxon object of the lowest common ancestor (LCA) of the inputs.

    Raises
    ------
    LCAError
        If the input list has less than two Taxon objects.
    """
    if len(taxon_list) < 2:
        raise LCAError("The input list must contain at least two Taxon objects.")
    lineage_list = [taxon.taxid_lineage for taxon in taxon_list]
    overlap = set.intersection(*map(set, lineage_list))
    for taxid in lineage_list[0]:
        if taxid in overlap:
            aggregated_taxa = [taxon.taxid for taxon in taxon_list]
            return _AggregatedTaxon(taxid, taxdb, 1.0, aggregated_taxa)
    return _AggregatedTaxon(1, taxdb, 1.0, [])


def find_majority_vote(
    taxon_list: List[Taxon],
    taxdb: TaxDb,
    fraction: float = 0.5,
    weights: Optional[List[float]] = None,
) -> Taxon:
    """
    Takes a list of multiple Taxon objects and returns the most specific taxon
    that is shared by more than the chosen fraction of the input lineages.

    Parameters
    ----------
    taxon_list : list
        A list containing at least two Taxon objects.
    taxdb : TaxDb
        A TaxDb object.
    fraction: float, default 0.5
        The returned taxon will be shared by more than `fraction` of the input
        taxa lineages. This value must be greater than 0.0 and less than 1.0.
    weights: list, optional
        A list of weights associated with the taxa lineages in `taxon_list`.
        These values are used to weight the votes of their associated lineages.

    Returns
    -------
    _AggregatedTaxon
        The _AggregatedTaxon object of the most specific taxon that is shared by
        more than a specified fraction of the input lineages.

    Raises
    ------
    MajorityVoteError
        If the input taxon list has less than two Taxon objects or if the
        `fraction` parameter is less than or equal to 0.0 or greater than or
        equal to 1.
    """
    if fraction <= 0.0 or fraction >= 1:
        raise MajorityVoteError(
            "The `fraction` parameter must be greater than 0.0 and less than 1."
        )
    if len(taxon_list) < 2:
        raise MajorityVoteError(
            "The input taxon list must contain at least two Taxon objects."
        )
    if weights and len(taxon_list) != len(weights):
        raise MajorityVoteError(
            "The input taxon and weights lists must have the same length."
        )
    if weights:
        return _weighted_majority_vote(taxon_list, taxdb, fraction, weights)
    else:
        return _unweighted_majority_vote(taxon_list, taxdb, fraction)
    return _AggregatedTaxon(1, taxdb, 1.0, [])


def _weighted_majority_vote(
    taxon_list: List[Taxon],
    taxdb: TaxDb,
    fraction: float = 0.5,
    weights: Optional[List[float]] = None,
) -> Taxon:
    """
    Takes a list of multiple Taxon objects and returns the most specific taxon
    that is shared by more than the chosen fraction of the input lineages.

    Parameters
    ----------
    taxon_list : list
        A list containing at least two Taxon objects.
    taxdb : TaxDb
        A TaxDb object.
    fraction: float, default 0.5
        The returned taxon will be shared by more than `fraction` of the input
        taxa lineages. This value must be greater than 0.0 and less than 1.
    weights: list, optional
        A list of weights associated with the taxa lineages in `taxon_list`.
        These values are used to weight the votes of their associated lineages.

    Returns
    -------
    _AggregatedTaxon
        The _AggregatedTaxon object of the most specific taxon that is shared by
        more than a specified fraction of the input lineages.
    """
    total_weight = sum(weights)
    zipped_taxid_lineage = list(
        zip_longest(*[reversed(i.taxid_lineage) for i in taxon_list])
    )
    for taxonomic_level in reversed(zipped_taxid_lineage):
        majority_taxon = defaultdict(float)
        for taxon, weight in zip(taxonomic_level, weights):
            majority_taxon[taxon] += weight
        majority_taxon = sorted(
            majority_taxon.items(), key=lambda x: x[1], reverse=True
        )
        if majority_taxon[0][0] and majority_taxon[0][1] > total_weight * fraction:
            agreement = majority_taxon[0][1] / total_weight
            aggregated_taxa = [taxon.taxid for taxon in taxon_list]
            if len(majority_taxon) > 1 and majority_taxon[0][1] > majority_taxon[1][1]:
                return _AggregatedTaxon(
                    majority_taxon[0][0], taxdb, agreement, aggregated_taxa
                )
            elif len(majority_taxon) == 1:
                return _AggregatedTaxon(
                    majority_taxon[0][0], taxdb, agreement, aggregated_taxa
                )


def _unweighted_majority_vote(
    taxon_list: List[Taxon], taxdb: TaxDb, fraction: float = 0.5
) -> Taxon:
    """
    Takes a list of multiple Taxon objects and returns the most specific taxon
    that is shared by more than the chosen fraction of the input lineages.

    Parameters
    ----------
    taxon_list : list
        A list containing at least two Taxon objects.
    taxdb : TaxDb
        A TaxDb object.
    fraction: float, default 0.5
        The returned taxon will be shared by more than `fraction` of the input
        taxa lineages. This value must be greater than 0.0 and less than 1.

    Returns
    -------
    _AggregatedTaxon
        The _AggregatedTaxon object of the most specific taxon that is shared by
        more than a specified fraction of the input lineages.
    """
    n_taxa = len(taxon_list)
    zipped_taxid_lineage = list(
        zip_longest(*[reversed(i.taxid_lineage) for i in taxon_list])
    )
    for taxonomic_level in reversed(zipped_taxid_lineage):
        majority_taxon = Counter(taxonomic_level).most_common()
        if majority_taxon[0][0] and majority_taxon[0][1] > n_taxa * fraction:
            agreement = majority_taxon[0][1] / n_taxa
            aggregated_taxa = [taxon.taxid for taxon in taxon_list]
            if len(majority_taxon) > 1 and majority_taxon[0][1] > majority_taxon[1][1]:
                return _AggregatedTaxon(
                    majority_taxon[0][0], taxdb, agreement, aggregated_taxa
                )
            elif len(majority_taxon) == 1:
                return _AggregatedTaxon(
                    majority_taxon[0][0], taxdb, agreement, aggregated_taxa
                )
