from groupy.base._scattering_mat_class import ScatteringMatrix
from pathlib import Path
import pytest
import numpy as np
import ENDFtk


@pytest.fixture
def U238_356_file():
    filename = Path(__file__).parent / "files" / "U238_356"
    return filename


@pytest.fixture
def U238_356(U238_356_file):
    tape = ENDFtk.tree.Tape.from_file(str(U238_356_file))
    mat = tape.material(tape.material_numbers[0])
    mf6 = mat.file(6)
    return mf6


def test_u238_elastic_scattering_matrix(U238_356):

    lines = U238_356.section(2).content.splitlines()
    obj = ScatteringMatrix(lines)

    assert obj.ZA == 92238
    assert obj.mt == 2
    assert obj.number_groups == 30
    assert obj.number_legendre == 5
    assert obj.temperature == 293

    assert obj.flux_values[0, 0] == 1.057475e-1
    assert obj.values[4, 3, 0] == 7.07267e-2


def test_u238_n2n_scattering_matrix(U238_356):

    scat_mat_lines = U238_356.section(16).content.splitlines()

    obj = ScatteringMatrix(scat_mat_lines)

    assert obj.ZA == 92238
    assert obj.mt == 16
    assert obj.number_groups == 30
    assert obj.number_legendre == 5
    assert obj.temperature == 293

    assert obj.values[4, 3, 0] == 0
    assert obj.values[25 - 1, 6 - 1, 0] == 2.033472e-7
    assert np.isclose(obj.values[25 - 1, 6 - 1, 4], -9.4936e-11)
