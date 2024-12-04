from groupy.base._energy_class import EnergyBoundaryValues
from pathlib import Path
import pytest


@pytest.fixture
def U238_356_file():
    filename = Path(__file__).parent / "files" / "U238_356"
    return filename


def test_u238_energies(U238_356_file):
    assert U238_356_file.exists()
    with open(U238_356_file, "r") as f:
        lines = f.readlines()

    energy_lines = lines[1:10]

    obj = EnergyBoundaryValues(energy_lines)
    assert obj.ZA == 92238

    assert obj.number_groups == 30
    assert obj.group_types == "neutron"
    assert obj.sigma0 == 1e10
    assert len(obj.energy_boundaries) == obj.number_groups + 1
    assert obj.energy_boundaries[-1] == 1.7e7
