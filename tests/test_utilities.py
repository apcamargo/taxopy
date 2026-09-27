import pytest

import taxopy
from taxopy.exceptions import LCAError, MajorityVoteError


@pytest.mark.network
def test_taxid_from_name_handles_exact_matches_homonyms_and_missing_names(ncbi_taxdb):
    assert taxopy.taxid_from_name("Homo sapiens", ncbi_taxdb) == [9606]
    assert sorted(taxopy.taxid_from_name("Aotus", ncbi_taxdb)) == [9504, 114498]

    with pytest.warns(Warning, match="not found in the taxonomy database"):
        assert taxopy.taxid_from_name(
            ["Homininae", "definitely-not-a-real-taxon"], ncbi_taxdb
        ) == [
            [207598],
            [],
        ]


@pytest.mark.network
def test_find_lca_returns_the_lowest_shared_taxon(ncbi_taxdb):
    human = taxopy.Taxon(9606, ncbi_taxdb)
    lagomorpha = taxopy.Taxon(9975, ncbi_taxdb)

    lca = taxopy.find_lca([human, lagomorpha], ncbi_taxdb)

    assert lca.taxid == 314146
    assert lca.name == "Euarchontoglires"


@pytest.mark.network
def test_find_lca_requires_multiple_taxa(ncbi_taxdb):
    human = taxopy.Taxon(9606, ncbi_taxdb)

    with pytest.raises(LCAError, match="at least two Taxon objects"):
        taxopy.find_lca([human], ncbi_taxdb)


@pytest.mark.network
def test_find_majority_vote_supports_unweighted_and_weighted_consensus(ncbi_taxdb):
    human = taxopy.Taxon(9606, ncbi_taxdb)
    gorilla = taxopy.Taxon(9593, ncbi_taxdb)
    lagomorpha = taxopy.Taxon(9975, ncbi_taxdb)
    yeast = taxopy.Taxon(4930, ncbi_taxdb)

    majority_vote = taxopy.find_majority_vote([human, gorilla, lagomorpha], ncbi_taxdb)
    weighted_majority_vote = taxopy.find_majority_vote(
        [yeast, human, gorilla, lagomorpha],
        ncbi_taxdb,
        weights=[3, 1, 1, 1],
    )

    assert majority_vote.taxid == 207598
    assert majority_vote.name == "Homininae"
    assert weighted_majority_vote.name == "Opisthokonta"


@pytest.mark.network
def test_find_majority_vote_validates_inputs(ncbi_taxdb):
    human = taxopy.Taxon(9606, ncbi_taxdb)
    gorilla = taxopy.Taxon(9593, ncbi_taxdb)

    with pytest.raises(MajorityVoteError, match="greater than 0.0 and less than 1"):
        taxopy.find_majority_vote([human, gorilla], ncbi_taxdb, fraction=1.0)

    with pytest.raises(MajorityVoteError, match="same length"):
        taxopy.find_majority_vote([human, gorilla], ncbi_taxdb, weights=[1.0])
