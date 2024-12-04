from groupy.base._pointwise_class import PointwiseValues
from pathlib import Path
import pytest
import numpy as np


@pytest.fixture
def U238_356_file():
    filename = Path(__file__).parent / "files" / "U238_356"
    return filename


def test_u238_energies(U238_356_file):
    assert U238_356_file.exists()
    with open(U238_356_file, "r") as f:
        lines = f.readlines()

    mf3mt1_lines = lines[10:72]

    obj = PointwiseValues(mf3mt1_lines)

    assert obj.ZA == 92238
    assert obj.mt == 1
    assert obj.number_groups == 30
    assert obj.number_legendre == 1
    assert len(obj.values) == obj.number_groups
    assert np.isclose(obj.temperature, 293)
    assert np.isclose(obj.values[0], 1.105207e1)
    assert np.isclose(obj.flux_values[0], 1.057475e-1)
