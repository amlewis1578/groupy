from groupy import run_njoy, GrouprOutput
import ENDFtk
from pathlib import Path


def get_grouped_data(
    endf6_file,
    title,
    directory=".",
    temperature=293,
    reconr_tolerance=0.001,
    broadr_tolerance=0.001,
    group_boundaries=2,
    flux=5,
    legendre_order=1,
    verbose=False,
):
    """Function to create an njoy input file and run njoy, then parse
    the GROUPR output and return a GrouprOutput object.

    Parameters
    ----------
    endf6_file : str or pathlib.Path object
        the ENDF6-formatted file

    title : str
        the run title

    directory : str, optional, default is '.'
        the directory in which to run NJOY. Default is the current
        directory.

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


    legendre_order : int, optional, default is 1
        the order to reconstruct the angular distributions


    verbose : bool, optional, default is False
        If true, extra information will be printed to the screen

    Returns
    --------
    GrouprOutput object
        the data parsed from NJOY
    """

    directory = Path(directory)

    # call run njoy
    run_njoy(
        endf6_file,
        title,
        directory,
        temperature,
        reconr_tolerance,
        broadr_tolerance,
        group_boundaries,
        flux,
        legendre_order,
        verbose,
    )

    # collect the output
    gendf_file = directory / "tape91"
    obj = GrouprOutput(gendf_file)

    # write the output files
    obj.write_to_csv(directory=directory, verbose=verbose)

    return obj
