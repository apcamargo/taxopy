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

from collections import Counter
from itertools import zip_longest
from taxopy.core import TaxDb, Taxon
from taxopy.exceptions import LCAError, MajorityVoteError


def find_lca(taxon_list: list, taxdb: TaxDb):
    """
    Takes a list of multiple Taxon objects and returns their lowest common
    ancestor (LCA).

    Parameters
    ----------
    taxon_list : list
        A list containing at least two Taxon objects.
    destination : TaxDb
        A TaxDb object.

    Returns
    -------
    Taxon
        The Taxon object of the lowest common ancestor (LCA) of the inputs.

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
            return Taxon(taxid, taxdb)


def find_majority_vote(taxon_list: list, taxdb: TaxDb):
    """
    Takes a list of multiple Taxon objects and returns the most specific taxon
    that is shared by more than half of the input lineages.

    Parameters
    ----------
    taxon_list : list
        A list containing at least two Taxon objects.
    destination : TaxDb
        A TaxDb object.

    Returns
    -------
    Taxon
        The Taxon object of the most specific taxon that is shared by more than
        half of the input lineages.

    Raises
    ------
    MajorityVoteError
        If the input list has less than three Taxon objects.
    """
    if len(taxon_list) < 3:
        raise MajorityVoteError(
            "The input list must contain at least three Taxon objects."
        )
    n_taxa = len(taxon_list)
    zipped_taxid_lineage = zip_longest(*[reversed(i.taxid_lineage) for i in taxon_list])
    for taxonomic_level in reversed(list(zipped_taxid_lineage)):
        majority_taxon = Counter(taxonomic_level).most_common()[0]
        if majority_taxon[1] > n_taxa / 2:
            return Taxon(majority_taxon[0], taxdb)
