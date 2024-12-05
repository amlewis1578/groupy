from groupy.base._outgoing_class import OutgoingDistribution
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
    mf = mat.file(5)
    return mf


def test_u238_pfns(U238_356):

    pfns_lines = U238_356.section(18).content.splitlines()

    obj = OutgoingDistribution(pfns_lines)

    assert obj.ZA == 92238
    assert obj.mt == 18
    assert obj.number_groups == 30
    assert obj.number_legendre == 1
    assert obj.temperature == 293
    assert len(obj.values) == obj.number_groups
    assert np.isclose(obj.temperature, 293)
    assert obj.values[0] == 2.43155e-12
    assert obj.values[-1] == 1.474703e-5
