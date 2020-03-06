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

from taxopy.core import TaxDb, Taxon
from taxopy.exceptions import DownloadError, ExtractionError, LCAError


def find_lca(taxon_list: list, taxdb: TaxDb):
    """
    Takes a list of multiple Taxon objects and computes their lowest common ancestor (LCA).

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
