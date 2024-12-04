import fortranformat as ff
import numpy as np


class ScatteringMatrix:
    """Class to hold a scattering matrix

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

        if mf != 6:
            raise ValueError(f"Outgoing distributions must come from MF6, not MF{mf}")

        # check that there is only 1 sigma0 value
        if nz != 1:
            raise NotImplementedError(
                f"Multiple sigma0 values are not yet implemented."
            )

        self.mt = mt
        self.number_groups = ngn
        self.number_legendre = nl

        self.values = np.zeros(
            (self.number_groups, self.number_groups, self.number_legendre)
        )
        self.flux_values = np.zeros((self.number_groups, self.number_legendre))

        matrix_lines = lines[1:]
        while len(matrix_lines) > 1:
            temp, _, ng2, ig2l0, nw, ig, _, _, _, _ = control_line.read(
                matrix_lines.pop(0)
            )
            num_value_lines = int(np.ceil(nw / 6))
            # print(f"ig: {ig} {ng2} {nw} {num_value_lines}")
            vals = []
            for j in range(num_value_lines):
                for val in value_line.read(matrix_lines.pop(0)):
                    vals.append(val)

            # row index is [IG-1], col indices are [IG2LO-1 : IG2LO-1 + NG2-1]

            # the flux values are the first (NLxNZ) values
            self.flux_values[ig - 1, :] = vals[: self.number_legendre]

            # the rest are the matrix values - there are (NLxNZ) in each
            # column
            for k in range(ng2 - 1):
                col_index = ig2l0 - 1 + k
                self.values[ig - 1, col_index, :] = vals[
                    (k + 1) * self.number_legendre : (k + 2) * self.number_legendre
                ]

        self.temperature = temp
