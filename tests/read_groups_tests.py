import pytest
from groupy import GrouprOutput
from pathlib import Path
import numpy as np


@pytest.fixture
def output_file():
    return Path(__file__).parent / "files" / "one_group"


def test_read_one_group(output_file):
    obj = GrouprOutput(output_file)

    assert obj._energy_boundaries.number_groups == 1
    assert np.array_equal([1e-5, 2e7], obj.energy_boundaries)
