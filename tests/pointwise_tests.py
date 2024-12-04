from groupy.base._pointwise_class import PointwiseValues
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
    mf = mat.file(3)
    return mf


def test_u238_total(U238_356):

    mf3mt1_lines = U238_356.section(1).content.splitlines()

    obj = PointwiseValues(mf3mt1_lines)

    assert obj.ZA == 92238
    assert obj.mt == 1
    assert obj.number_groups == 30
    assert obj.number_legendre == 1
    assert len(obj.values) == obj.number_groups
    assert np.isclose(obj.temperature, 293)
    assert np.isclose(obj.values[0], 1.105207e1)
    assert np.isclose(obj.flux_values[0], 1.057475e-1)


def test_u238_nubar(U238_356):

    nubar_lines = U238_356.section(452).content.splitlines()

    obj = PointwiseValues(nubar_lines)

    assert obj.ZA == 92238
    assert obj.mt == 452
    assert obj.number_groups == 30
    assert obj.number_legendre == 1
    assert len(obj.values) == obj.number_groups
    assert np.isclose(obj.temperature, 293)
    assert np.isclose(obj.values[0], 2.443041)
    assert np.isclose(obj.flux_values[0], 1.057475e-1)


def test_u238_n2n(U238_356):

    n2n_lines = U238_356.section(16).content.splitlines()

    obj = PointwiseValues(n2n_lines)

    assert obj.ZA == 92238
    assert obj.mt == 16
    assert obj.number_groups == 30
    assert obj.number_legendre == 1
    assert len(obj.values) == obj.number_groups
    assert np.isclose(obj.temperature, 293)
    assert obj.values[0] == 0
    assert obj.values[23] == 0
    assert np.isclose(obj.values[24], 3.38396e-1)
