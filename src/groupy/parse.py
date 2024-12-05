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

        for mf in mat.file_numbers.to_list():

            # get the energies from MF1 MT451
            if mf == 1:

                mf1_mt451 = mat.file(mf).section(451).content.splitlines()
                self._energy_boundaries = EnergyBoundaryValues(mf1_mt451)

            # go through the pointwise (MF3)
            elif mf == 3:
                self.pointwise = {}
                mf3 = mat.file(mf)
                for mt in mf3.section_numbers.to_list():
                    lines = mf3.section(mt).content.splitlines()
                    self.pointwise[mt] = PointwiseValues(lines)

            # go through distributions (MF5)
            elif mf == 5:
                self.outgoing_distributions = {}
                mf5 = mat.file(mf)
                for mt in mf5.section_numbers.to_list():
                    lines = mf5.section(mt).content.splitlines()
                    self.outgoing_distributions[mt] = OutgoingDistribution(lines)

            # go through scattering matrices (MF6)
            elif mf == 6:
                self.scattering_matrices = {}
                mf6 = mat.file(mf)
                for mt in mf6.section_numbers.to_list():
                    lines = mf6.section(mt).content.splitlines()
                    self.scattering_matrices[mt] = ScatteringMatrix(lines)

            else:
                raise NotImplementedError(f"GrouprOutput can't yet parse MF{mf}")
