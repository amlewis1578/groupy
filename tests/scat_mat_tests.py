from groupy.base._scattering_mat_class import ScatteringMatrix
from pathlib import Path
import pytest
import numpy as np


@pytest.fixture
def U238_356_file():
    filename = Path(__file__).parent / "files" / "U238_356"
    return filename


def test_u238_elastic_scattering_matrix(U238_356_file):
    assert U238_356_file.exists()
    with open(U238_356_file, "r") as f:
        lines = f.readlines()

    scat_mat_lines = lines[240:361]

    obj = ScatteringMatrix(scat_mat_lines)

    assert obj.ZA == 92238
    assert obj.mt == 2
    assert obj.number_groups == 30
    assert obj.number_legendre == 5
    assert obj.temperature == 293

    assert obj.flux_values[0, 0] == 1.057475e-1
    assert obj.values[4, 3, 0] == 7.07267e-2


def test_u238_n2n_scattering_matrix(U238_356_file):
    assert U238_356_file.exists()
    with open(U238_356_file, "r") as f:
        lines = f.readlines()

    scat_mat_lines = lines[361:481]

    obj = ScatteringMatrix(scat_mat_lines)

    assert obj.ZA == 92238
    assert obj.mt == 16
    assert obj.number_groups == 30
    assert obj.number_legendre == 5
    assert obj.temperature == 293

    assert obj.values[4, 3, 0] == 0
    assert obj.values[25 - 1, 6 - 1, 0] == 2.033472e-7
    assert np.isclose(obj.values[25 - 1, 6 - 1, 4], -9.4936e-11)
