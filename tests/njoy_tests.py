from groupy import run_njoy
from groupy.njoy import write_njoy_input
from pathlib import Path
import pytest
import ENDFtk
import numpy as np


@pytest.fixture
def U238_endf_file():
    filename = Path(__file__).parent / "files" / "n-092_U_238.endf"
    return filename


@pytest.fixture
def U238_input():
    filename = Path(__file__).parent / "files" / "input_u238_356"
    return filename


@pytest.fixture
def U238_356():
    filename = Path(__file__).parent / "files" / "U238_356"
    return filename


@pytest.fixture(scope="session")
def test_dir(tmpdir_factory):
    test_dir = tmpdir_factory.mktemp("groupr")
    return test_dir


def test_njoy_lines_U238_356(U238_input):
    mat = 9237
    title = "test with 238U"
    reconr_tol = 0.01
    result = write_njoy_input(
        mat,
        title,
        reconr_tolerance=reconr_tol,
        has_nubar=True,
        has_pfns=True,
        group_boundaries=3,
        legendre_order=1,
    )

    with open(U238_input, "r") as f:
        ans = f.read()

    assert result == ans[: len(result)]


def test_njoy_lines():
    mat = 9237
    title = "test2 with 238U"
    reconr_tol = 0.01
    broadr_tol = 0.0001
    temp = 600
    has_nubar = False
    has_pfns = False
    group_boundaries = [1e-5, 1e3, 1e5, 2e7]
    ign = 1
    flux = 11
    legendre = 2
    result = write_njoy_input(
        mat,
        title,
        temperature=temp,
        reconr_tolerance=reconr_tol,
        broadr_tolerance=broadr_tol,
        has_nubar=has_nubar,
        has_pfns=has_pfns,
        group_boundaries=group_boundaries,
        flux=flux,
        legendre_order=legendre,
    )

    ans = f""" -- 
 -- {title}
 --
 reconr
  20 21/
  'pendf tape for {title}' /
  {mat} 0 / mat ; num extra points
  {reconr_tol} / tolerance 
  0 /
 --
 --
 broadr
  20 21 22 /
  {mat} 1 / mat ; num temps
  {broadr_tol} / tolerance
  {temp} / temperature [K]
  0 /
 --
 --
 groupr
  20 22 0 91 /
  {mat} {ign} 0 {flux} {legendre} /
  '{title}' /
  {temp} /
  1.0e10 /
  {len(group_boundaries)-1}/ #
  {group_boundaries[0]:.5E} {group_boundaries[1]:.5E} {group_boundaries[2]:.5E} {group_boundaries[3]:.5E} /
  3 /
  6 / scattering matrices 
  0 /
  0 /
 --
 --
 stop
 """

    assert result == ans[: len(result)]


@pytest.mark.slow
def test_create_U238_356(U238_endf_file, U238_input, U238_356, test_dir):
    title = "test with 238U"
    groups = 3
    reconr_tol = 0.01
    run_njoy(
        U238_endf_file,
        title,
        directory=test_dir,
        group_boundaries=groups,
        reconr_tolerance=reconr_tol,
        verbose=True,
    )

    njoy_input = test_dir / "input"
    assert njoy_input.exists()

    assert U238_input.read_text(encoding=None) == njoy_input.read_text(encoding=None)

    njoy_output = test_dir / "output"
    assert njoy_output.exists()

    assert title in njoy_output.read_text(encoding=None)


@pytest.mark.fishing
def test_all_njoy_input(test_dir):
    endf80_dir = Path("/home/amanda/libraries/endf80/")
    if not endf80_dir.exists():
        return None
    else:
        for fle in endf80_dir.glob("*.endf"):
            print(fle)
            tape = ENDFtk.tree.Tape.from_file(str(fle))
            mat_num = tape.material_numbers[0]
            write_njoy_input(mat_num, "")


@pytest.mark.fishing
def test_all_run_njoy(test_dir):
    endf80_dir = Path("/home/amanda/libraries/endf80/")
    if not endf80_dir.exists():
        return None
    else:
        for fle in endf80_dir.glob("*.endf"):
            print(fle)
            run_njoy(
                fle,
                "",
                directory=test_dir,
                reconr_tolerance=0.1,
                broadr_tolerance=0.1,
                group_boundaries=[1e-5, 2e7],
                legendre_order=1,
            )
