import os
import shutil

import pytest

import taxopy

NCBI_TAXDUMP_URL = "https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz"


def pytest_addoption(parser):
    parser.addoption(
        "--run-network",
        action="store_true",
        default=False,
        help="run tests that download the NCBI taxonomy dump",
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "network: requires downloading the NCBI taxonomy dump",
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-network"):
        return

    skip_network = pytest.mark.skip(
        reason="requires network access; run pytest with --run-network",
    )
    for item in items:
        if "network" in item.keywords:
            item.add_marker(skip_network)


@pytest.fixture(scope="session")
def ncbi_taxdb(tmp_path_factory):
    taxdb_dir = tmp_path_factory.mktemp("taxdb")
    taxdump_url = os.environ.get("TAXOPY_TEST_TAXDUMP_URL", NCBI_TAXDUMP_URL)

    try:
        taxdb = taxopy.TaxDb(
            taxdb_dir=str(taxdb_dir),
            taxdump_url=taxdump_url,
        )
    except Exception:
        shutil.rmtree(taxdb_dir, ignore_errors=True)
        raise

    yield taxdb

    shutil.rmtree(taxdb_dir, ignore_errors=True)
