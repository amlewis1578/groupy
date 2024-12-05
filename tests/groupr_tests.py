from groupy import GrouprOutput
from pathlib import Path
import pytest
import numpy as np


@pytest.fixture
def U238_356_file():
    filename = Path(__file__).parent / "files" / "U238_356"
    return filename


def test_U238_356(U238_356_file):
    obj = GrouprOutput(U238_356_file)

    assert obj.material_number == 9237

    assert obj.energy_boundaries[0] == 1.390000e-4

    assert len(obj.pointwise) == 5
    assert obj.pointwise[16].values[0] == 0
    assert obj.outgoing_distributions[18].values[0] == 2.43155e-12
    assert obj.scattering_matrices[2].values[4, 3, 0] == 7.07267e-2
