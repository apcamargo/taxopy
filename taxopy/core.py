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

import os
import tarfile
import urllib.request

from taxopy.exceptions import DownloadError, ExtractionError, TaxidError


class TaxDb:
    """
    Create an object of the TaxDb class.

    Parameters
    ----------
    taxdb_dir : str, optional
        A directory to download NCBI's taxonomy database files to. If the
        directory does not exist it will be created.
    nodes_dmp : str, optional
        The path for a pre-downloaded `nodes.dmp` file. If both `nodes.dmp` and
        `names.dmp` are supplied NCBI's taxonomy database won't be downloaded.
    names_dmp : str, optional
        The path for a pre-downloaded `names.dmp` file. If both `names.dmp` and
        `nodes.dmp` are supplied NCBI's taxonomy database won't be downloaded.
    keep_files : bool, default True
        Keep the `nodes.dmp` and `names.dmp` files after the TaxDb object is
        created. If `taxdb_dir` was supplied the whole directory will be deleted.
        By default, the files are deleted.


    Attributes
    ----------
    taxid2name : dict
        A dictionary where the keys are taxonomic identifiers and the values are
        their corresponding names.
    taxid2parent: dict
        A dictionary where the keys are taxonomic identifiers and the values are
        the taxonomic identifiers of their corresponding parent taxon.
    taxid2rank: dict
        A dictionary where the keys are taxonomic identifiers and the values are
        their corresponding ranks.

    Raises
    ------
    DownloadError
        If the download of the taxonomy database fails.
    ExtractionError
        If the decompression of the taxonomy database fails.
    """

    def __init__(
        self,
        *,
        taxdb_dir: str = None,
        nodes_dmp: str = None,
        names_dmp: str = None,
        keep_files: bool = False
    ):
        if not taxdb_dir:
            self._taxdb_dir = os.getcwd()
        elif not os.path.isdir(taxdb_dir):
            os.makedirs(taxdb_dir)
            self._taxdb_dir = taxdb_dir
        else:
            self._taxdb_dir = taxdb_dir
        if not (nodes_dmp and names_dmp):
            self._nodes_dmp, self._names_dmp = self._download_taxonomy()
        else:
            self._nodes_dmp, self._names_dmp = nodes_dmp, names_dmp
        self.taxid2parent, self.taxid2rank = self._import_nodes()
        self.taxid2name = self._import_names()
        if not keep_files:
            self._delete_files()

    def _download_taxonomy(self):
        url = "ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz"
        tmp_taxonomy_file = os.path.join(self._taxdb_dir, "taxdump.tar.gz")
        try:
            urllib.request.urlretrieve(url, tmp_taxonomy_file)
        except:
            raise DownloadError(
                "Download of taxonomy files failed. NCBI's server may be offline."
            )
        try:
            with tarfile.open(tmp_taxonomy_file) as tf:
                tf.extract("nodes.dmp", path=self._taxdb_dir)
                tf.extract("names.dmp", path=self._taxdb_dir)
        except:
            raise ExtractionError(
                "Something went wrong while extracting the taxonomy files."
            )
        os.remove(tmp_taxonomy_file)
        return (
            os.path.join(self._taxdb_dir, "nodes.dmp"),
            os.path.join(self._taxdb_dir, "names.dmp"),
        )

    def _import_nodes(self):
        taxid2parent = {}
        taxid2rank = {}
        with open(self._nodes_dmp, "r") as f:
            for line in f:
                line = line.split("\t")
                taxid = line[0]
                parent = line[2]
                rank = line[4]
                taxid2parent[taxid] = parent
                taxid2rank[taxid] = rank
        return taxid2parent, taxid2rank

    def _import_names(self):
        taxid2name = {}
        with open(self._names_dmp, "r") as f:
            for line in f:
                line = line.split("\t")
                if line[6] == "scientific name":
                    taxid = line[0]
                    name = line[2]
                    taxid2name[taxid] = name
        return taxid2name

    def _delete_files(self):
        os.remove(self._nodes_dmp)
        os.remove(self._names_dmp)
        if not os.listdir(self._taxdb_dir) and self._taxdb_dir != os.getcwd():
            os.rmdir(self._taxdb_dir)


class Taxon:
    """
    Create an object of the Taxon class.

    Parameters
    ----------
    taxid : str
        A NCBI taxonomic identifier.
    taxdb : TaxDb
        A TaxDb object.

    Attributes
    ----------
    taxid : str
        The NCBI taxonomic identifier the object represents (e.g., '9606').
    name: str
        The name of the taxon (e.g., 'Homo sapiens').
    rank: str
        The rank of the taxon (e.g., 'species').
    taxid_lineage: list
        An ordered list containing the taxonomic identifiers of the whole lineage
        of the taxon, from the most specific to the most general.
    name_lineage: list
        An ordered list containing the names of the whole lineage of the taxon,
        from the most specific to the most general.
    rank_name_dictionary: dict
        A dictionary where the keys are named ranks and the values are the names
        of the taxa that correspond to each of the named ranks in the lineage.

    Raises
    ------
    TaxidError
        If the input string is not a valid NCBI taxonomic identifier.
    """

    def __init__(self, taxid: str, taxdb: TaxDb):
        self.taxid = taxid
        if self.taxid not in taxdb.taxid2name:
            raise TaxidError("The input string is not a valid NCBI taxonomic identifier.")
        self.name = taxdb.taxid2name[self.taxid]
        self.rank = taxdb.taxid2rank[self.taxid]
        self.taxid_lineage = self._find_lineage(taxdb.taxid2parent)
        self.name_lineage = self._convert_to_names(taxdb.taxid2rank, taxdb.taxid2name)
        self.rank_name_dictionary = self._convert_to_rank_name_dictionary(
            taxdb.taxid2rank, taxdb.taxid2name
        )

    def __repr__(self):
        return " > ".join(reversed(self.name_lineage))

    def _find_lineage(self, taxid2parent):
        lineage = []
        current_taxid = self.taxid
        lineage.append(current_taxid)
        while taxid2parent[current_taxid] != current_taxid:
            current_taxid = taxid2parent[current_taxid]
            lineage.append(current_taxid)
        return lineage

    def _convert_to_names(self, taxid2rank, taxid2name):
        names = []
        for taxid in self.taxid_lineage:
            name = taxid2name[taxid]
            names.append(name)
        return names

    def _convert_to_rank_name_dictionary(self, taxid2rank, taxid2name):
        rank_name_dictionary = {}
        for taxid in self.taxid_lineage:
            rank = taxid2rank[taxid]
            if rank != "no rank":
                rank_name_dictionary[rank] = taxid2name[taxid]
        return rank_name_dictionary
