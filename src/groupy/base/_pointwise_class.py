import fortranformat as ff
import numpy as np


class PointwiseValues:
    """Class to hold pointwise values like cross section and
    nubar

    Parameters
    ----------
    lines : list of strings
        the MF3 lines from the GENDF file

    Attributes
    ----------
    mt : int
        the MT number

    number_groups : int
        the number of groups

    values : np.array of floats
        the values (in barns for cross sections)

    number_legendre : int
        the number of Legendre coeffs used in the calculation

    flux_values : np.array of floats
        the flux values

    temperature : float
        the temperature of the calculation in K

    ZA : int
        the isotope ZA


    Methods
    -------
    parse_lines
        Function to parse the lines

    """

    def __init__(self, lines):

        self.parse_lines(lines)

    def parse_lines(self, lines):
        """Function to parse the lines

        Parameters
        ----------
        lines : list of strings
            the lines from the GENDF file

        Returns
        -------
        None

        """
        control_line = ff.FortranRecordReader("(2G11.0,4I11,I4,I2,I3,I5)")
        value_line = ff.FortranRecordReader("(2G11.0)")

        self.ZA, _, nl, nz, lrflag, ngn, mat, mf, mt, _ = control_line.read(lines[0])

        if mf != 3:
            raise ValueError(f"PointwiseValues must come from MF3, not MF{mf}")

        # check that there is only 1 sigma0 value
        if nz != 1:
            raise NotImplementedError(
                f"Multiple sigma0 values are not yet implemented."
            )

        self.mt = mt
        self.number_groups = ngn
        self.number_legendre = nl

        self.values = np.zeros(self.number_groups)
        self.flux_values = np.zeros(self.number_groups)
        for i in range(self.number_groups):
            temp, _, ng2, ig2lo, nw, ig, _, _, _, _ = control_line.read(
                lines[2 * i + 1]
            )
            flux, sigma = value_line.read(lines[2 * i + 2])
            self.values[ig - 1] = sigma
            self.flux_values[ig - 1] = flux

            if ig == self.number_groups:
                break

        self.temperature = temp
