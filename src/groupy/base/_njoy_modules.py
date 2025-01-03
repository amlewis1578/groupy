import numpy as np


def make_reconr(mat, title, tolerance=0.001):
    """Function to write a reconr input

    Parameters
    ----------
    mat : int
        material number

    title : str
        title for the run

    tolerance : float, optional, default is 0.001
        the tolerance for reconstruction

    Returns
    -------
    str
        the lines for the input file
    """

    input = " reconr\n"
    input += f"  20 21/\n"
    input += f"  'pendf tape for {title}' /\n"
    input += f"  {mat} 0 / mat ; num extra points\n"
    input += f"  {tolerance} / tolerance \n"
    input += "  0 /\n --\n --\n"
    return input


def make_broadr(mat, temp, tolerance=0.001):
    """Function to write a broadr input

    Parameters
    ----------
    mat : int
        material number

    temp : int or float
        temperature for the run in K

    tolerance : float, optional, default is 0.001
        the tolerance for broadening

    Returns
    -------
    str
        the lines for the input file
    """

    input = " broadr\n"
    input += f"  20 21 22 /\n"
    input += f"  {mat} 1 / mat ; num temps\n"
    input += f"  {tolerance} / tolerance\n"
    input += f"  {temp} / temperature [K]\n"
    input += "  0 /\n --\n --\n"
    return input


def make_groupr(
    mat,
    temp,
    title,
    group_boundaries,
    flux,
    has_nubar=False,
    has_pfns=False,
    legendre_order=4,
):
    """Function to write a groupr input

    Parameters
    ----------
    mat : int
        material number

    temp : int or float
        temperature for the run in K

    title : str
        title for the run

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
    -------
    str
        the lines for the input file
    """

    try:
        ign = int(group_boundaries)
        if ign > 34:
            raise ValueError(f"Neutron group number {ign} is not allowed.")
    except TypeError:
        ign = 1

    try:
        iwt = int(flux)
        if iwt not in [2, 3, 5, 9, 11]:
            raise ValueError(f"Flux number {iwt} is not allowed.")
    except TypeError:
        raise TypeError(f"the flux paramter must be an integer.")

    input = " groupr\n"
    input += f"  20 22 0 91 /\n"
    input += f"  {mat} {ign} 0 {iwt} {legendre_order} /\n"
    input += f"  '{title}' /\n"
    input += f"  {temp} /\n"
    input += "  1.0e10 /\n"

    # group boundaries - split into lines 5 long
    if ign == 1:
        input += f"  {len(group_boundaries)-1}/ #\n"
        for i in range(int(np.ceil(len(group_boundaries) / 5))):
            input += "  "
            for j in range(5):
                try:
                    input += f"{group_boundaries[i*5+j]:.5E} "
                except IndexError:
                    input += "/"
                    break
                if (i + 1) * (j + 1) == len(group_boundaries):
                    input += "/"
                    break
            input += "\n"

    input += "  3 /\n"
    if has_nubar:
        input += "  3 452 'total nubar' /\n"
    if has_pfns:
        input += "  5 18 'pfns' /\n"
    input += "  6 / scattering matrices \n"
    input += "  0 /\n"
    input += "  0 /\n --\n --\n"
    return input
