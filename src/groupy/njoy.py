import ENDFtk
from pathlib import Path
from groupy.base._njoy_modules import *


def run_njoy(endf6_file, title, directory=".", verbose=False):
    """Function to create an njoy input file and run njoy

    Parameters
    ----------
    endf6_file : str or pathlib.Path object
        the ENDF6-formatted file

    title : str
        the run title

    directory : str, optional, default is '.'
        the directory in which to run NJOY. Default is the current
        directory.

    verbose : bool, optional, default is False
        If true, extra information will be printed to the screen

    Returns
    --------
    None
    """

    # check ENDF6 file
    endf6_file = Path(endf6_file).absolute()
    if not endf6_file.exists():
        raise FileNotFoundError(f"The ENDF6-formatted file {endf6_file} was not found.")

    # open with ENDFtk and get the important information
    tape = ENDFtk.tree.Tape.from_file(str(endf6_file))
    mat_num = tape.material_numbers[0]
    mat = tape.material(mat_num)
    if verbose:
        print(f"\nRunning NJOY for {mat_num}")

    # check for nubar
    if mat.file(1).has_MT(452):
        has_nubar = True
        if verbose:
            print(f"\t{mat_num} has nubar")
    else:
        has_nubar = False
        if verbose:
            print(f"\t{mat_num} does not have nubar")

    # check for PFNS
    if mat.file(5).has_MT(18):
        has_pfns = True
        if verbose:
            print(f"\t{mat_num} has PFNS")
    else:
        has_pfns = False
        if verbose:
            print(f"\t{mat_num} does not have PFNS")

    # input file
    input_file = Path(directory) / "input"
    if verbose:
        print(f" Input file: {input_file}")


def write_njoy_input(
    mat,
    title,
    temperature=293,
    reconr_tolerance=0.001,
    broadr_tolerance=0.001,
    group_boundaries=2,
    flux=5,
    has_nubar=False,
    has_pfns=False,
    legendre_order=4,
):
    """Function to create the strings for an njoy input file

    Parameters
    ----------
    mat : int
        the material number

    title : str
        the run title

    temperature : float, optional, default is 293 K
        the temperature of the run in K

    reconr_tolerance : float, optional, default is 0.001
        the tolerance for the reconr module

    broadr_tolerance : float, optional, default is 0.001
        the tolerance for the broader module

    group_boundaries : int or list
        The group boundaries to use. If an integer, it represents ign in the
        NJOY input. If a list, it is the energy boundaries in eV.

    flux : int
        The weighting flux to use - the iwt value in the NJOY input. Currently
        the only iwt values allowed are:
            2   constant
            3   1/e
            5   epri-cell lwr
            9   claw weight function
            11  vitamin-e weight function

    has_nubar : bool, optional, default is False
        whether or not the evaluation has nubar

    has_pfns : bool, optional, default is False
        whether or not the evaluation has a PFNS

    legendre_order : int, optional, default is 4
        the order to reconstruct the angular distributions


    Returns
    --------
    str
        the text for the input file
    """

    input = " -- \n -- "
    input += title
    input += "\n --\n"

    input += make_reconr(mat, title, reconr_tolerance)
    input += make_broadr(mat, temperature, broadr_tolerance)
    input += make_groupr(
        mat,
        temperature,
        title,
        group_boundaries,
        flux,
        legendre_order=legendre_order,
        has_nubar=has_nubar,
        has_pfns=has_pfns,
    )

    input += " stop"
    return input
