import ENDFtk
from pathlib import Path
from groupy.base._energy_class import EnergyBoundaryValues
from groupy.base._pointwise_class import PointwiseValues
from groupy.base._outgoing_class import OutgoingDistribution
from groupy.base._scattering_mat_class import ScatteringMatrix


class GrouprOutput:
    """Class to hold the full output of GROUPR

    Parameters
    ----------
    filename : str or pathlib.Path object
        the GENDF file


    Attributes
    ----------

    Methods
    -------

    """

    def __init__(self, filename):

        self.filename = Path(filename)

        # check that the file exists
        if not filename.exists():
            raise FileNotFoundError(f"The GENDF file {filename} was not found")

        # parse the file
        self.parse()

    @property
    def energy_boundaries(self):
        return self._energy_boundaries.energy_boundaries

    def parse(self):
        """Function to parse the full GENDF file

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        tape = ENDFtk.tree.Tape.from_file(str(self.filename))
        mat = tape.material(tape.material_numbers[0])
        self.material_number = mat.MAT

        # get the energies from MF1 MT451
        mf1_mt451 = mat.file(1).section(451).content.splitlines()
        self._energy_boundaries = EnergyBoundaryValues(mf1_mt451)

        # go through the pointwise (MF3)
        self.pointwise = {}
        mf3 = mat.file(3)
        for mt in mf3.section_numbers.to_list():
            lines = mf3.section(mt).content.splitlines()
            self.pointwise[mt] = PointwiseValues(lines)

        # go through distributions (MF5)
        self.outgoing_distributions = {}
        if mat.has_file(5):
            mf5 = mat.file(5)
            for mt in mf5.section_numbers.to_list():
                lines = mf5.section(mt).content.splitlines()
                self.outgoing_distributions[mt] = OutgoingDistribution(lines)

        # go through scattering matrices (MF6)
        self.scattering_matrices = {}
        if mat.has_file(6):
            mf6 = mat.file(6)
            for mt in mf6.section_numbers.to_list():
                lines = mf6.section(mt).content.splitlines()
                self.scattering_matrices[mt] = ScatteringMatrix(lines)
