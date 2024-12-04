import fortranformat as ff


class EnergyBoundaryValues:
    """Class to hold the group boundaries in eV

    Parameters
    ----------
    lines : list of strings
        the MF1 lines from the GENDF file

    Attributes
    ----------

    Methods
    -------

    """

    def __init__(self, lines):

        self.parse_lines(lines)

    def parse_lines(self, lines):
        control_line = ff.FortranRecordReader("(2G11.0,4I11,I4,I2,I3,I5)")
        energy_line = ff.FortranRecordReader("(6G11.0)")

        self.ZA, self.AWR, _, nz, _, _, _, mf, mt, _ = control_line.read(lines[0])

        # check that there is only 1 sigma0 value
        if nz != 1:
            raise NotImplementedError(
                f"Multiple sigma0 values are not yet implemented."
            )

        # check that MF and MT are correct
        if mf != 1 or mt != 451:
            raise ValueError(
                f"The EnergyBoundaryValues class must be given MF1 MT451 section, not the MT{mf} MT{mt} section."
            )

        # read the next control line
        temp, _, ngn, ngg, nw, _, _, _, _, _ = control_line.read(lines[1])

        # figure out neutron or gamma groups and get number
        if ngn > 0:
            self.number_groups = ngn
            self.group_types = "neutron"
        elif ngg > 0:
            self.number_groups = ngg
            self.group_types = "gamma"
        else:
            raise ValueError(f"Both NGN and NGG cannot be zero.")

        # read the group boundaries

        # the first line has zero and then sigma0 first
        vals = energy_line.read(lines[2])
        self.sigma0 = vals[1]
        self.energy_boundaries = vals[2:]

        for line in lines[3:-1]:
            for val in energy_line.read(line):
                if val > 0:
                    self.energy_boundaries.append(val)
