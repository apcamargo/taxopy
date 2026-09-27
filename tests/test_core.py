import pytest

import taxopy
from taxopy.exceptions import TaxidError


@pytest.mark.network
def test_taxdb_loads_known_taxonomy_records(ncbi_taxdb):
    assert ncbi_taxdb.taxid2name[9606] == "Homo sapiens"
    assert ncbi_taxdb.taxid2parent[9606] == 9605
    assert ncbi_taxdb.taxid2rank[9606] == "species"
    assert ncbi_taxdb.taxid2all_names[9606]["scientific name"] == ["Homo sapiens"]


@pytest.mark.network
def test_taxon_exposes_lineage_rank_lookup_and_parent(ncbi_taxdb):
    human = taxopy.Taxon(9606, ncbi_taxdb)

    assert human.name == "Homo sapiens"
    assert human.rank == "species"
    assert human.legacy_taxid is False
    assert human.name_lineage[:3] == ["Homo sapiens", "Homo", "Homininae"]
    assert human.rank_name_dictionary["genus"] == "Homo"
    assert human.rank_name_dictionary["family"] == "Hominidae"
    assert human.rank_name_dictionary["domain"] == "Eukaryota"
    assert human.parent(ncbi_taxdb).taxid == 9605


@pytest.mark.network
def test_taxon_supports_legacy_taxids(ncbi_taxdb):
    legacy_taxid, current_taxid = next(iter(ncbi_taxdb.oldtaxid2newtaxid.items()))

    legacy_taxon = taxopy.Taxon(legacy_taxid, ncbi_taxdb)
    current_taxon = taxopy.Taxon(current_taxid, ncbi_taxdb)

    assert legacy_taxon.legacy_taxid is True
    assert legacy_taxon.name == current_taxon.name
    assert legacy_taxon.rank == current_taxon.rank
    assert legacy_taxon.taxid_lineage[1:] == current_taxon.taxid_lineage[1:]


@pytest.mark.network
def test_taxon_rejects_invalid_taxids(ncbi_taxdb):
    with pytest.raises(TaxidError, match="not a valid NCBI taxonomic identifier"):
        taxopy.Taxon(-1, ncbi_taxdb)
