from groupy import GrouprOutput
from pathlib import Path
import pytest
import numpy as np


@pytest.fixture
def U238_356_file():
    filename = Path(__file__).parent / "files" / "U238_356"
    return filename


@pytest.fixture(scope="session")
def test_dir(tmpdir_factory):
    test_dir = tmpdir_factory.mktemp("groupr")
    return test_dir


def test_U238_356(U238_356_file, test_dir):
    obj = GrouprOutput(U238_356_file)

    assert obj.title == "test with 238U"

    assert obj.material_number == 9237

    assert obj.energy_boundaries[0] == 1.390000e-4

    assert len(obj.pointwise) == 53
    assert obj.pointwise[16].values[0] == 0
    assert obj.outgoing_distributions[18].values[0] == 2.43155e-12
    assert np.isclose(obj.scattering_matrices[2].values[4, 3, 0], 7.07267e-2, rtol=0.01)

    title = "testU238"
    obj.write_to_csv(title=title, verbose=True, directory=test_dir)

    pointwise = np.genfromtxt(test_dir / f"{title}_pointwise.csv", delimiter=",")
    assert pointwise[0, 0] == obj.energy_boundaries[0]
    assert pointwise[0, 1] == obj.pointwise[1].values[0]

    dists = np.genfromtxt(test_dir / f"{title}_outgoing.csv", delimiter=",")
    # print(dists)
    assert dists[0, 0] == obj.energy_boundaries[0]
    assert np.allclose(dists[:-1, 1], obj.outgoing_distributions[18].values)

    n2n_ell0 = np.genfromtxt(
        test_dir / f"{title}_scattering_matrix_16.csv", delimiter=","
    )
    assert n2n_ell0[0, 0] == 0
    assert np.array_equal(n2n_ell0[0, 1:], obj.energy_boundaries)
    assert np.array_equal(
        n2n_ell0[1:-1, 1:-1], obj.scattering_matrices[16].values[:, :, 0]
    )

    inel = np.genfromtxt(test_dir / f"{title}_scattering_matrix_4.csv", delimiter=",")
    assert inel[0, 1] == obj.energy_boundaries[0]
    assert inel[1, 0] == obj.energy_boundaries[0]
    total = np.zeros((len(obj.energy_boundaries), len(obj.energy_boundaries)))
    for mt in range(51, 92):
        if mt in obj.scattering_matrices.keys():
            total[:-1, :-1] += obj.scattering_matrices[mt].values[:, :, 0]

    assert np.allclose(total, inel[1:, 1:])
