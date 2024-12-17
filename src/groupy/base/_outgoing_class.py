import fortranformat as ff
import numpy as np


class OutgoingDistribution:
    """Class to hold outgoing energy or angle distributions

    Parameters
    ----------
    lines : list of strings
        the lines from the GENDF file

    Attributes
    ----------
    mt : int
        the MT number

    number_groups : int
        the number of groups

    values : np.array of floats
        the values

    number_legendre : int
        the number of Legendre coeffs used in the calculation

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
        value_line = ff.FortranRecordReader("(6G11.0)")

        self.ZA, _, nl, nz, lrflag, ngn, mat, mf, mt, _ = control_line.read(lines[0])

        if mf not in [5]:
            raise ValueError(f"Outgoing distributions must come from MF5, not MF{mf}")

        # check that there is only 1 sigma0 value
        if nz != 1:
            raise NotImplementedError(
                f"Multiple sigma0 values are not yet implemented."
            )

        self.mt = mt
        self.number_groups = ngn
        self.number_legendre = nl

        self.temperature, _, _, _, _, _, _, _, _, _ = control_line.read(lines[1])

        self.values = np.zeros(self.number_groups)

        for i in range(int(np.ceil(self.number_groups / 6))):
            vals = np.array(value_line.read(lines[2 + i]))
            self.values[i * 6 : (i + 1) * 6] = vals[vals > 0]
