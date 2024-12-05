import ENDFtk
from pathlib import Path
import numpy as np
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

        self.title = tape.content.splitlines()[0][:66].strip()

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

    def write_to_csv(self, title=None, directory=None, verbose=False):
        """Function to write the grouped values into CSV files.

        All of the pointwise values are written into {title}_pointwise.csv, with
            the MT values as the column headers.
        All of the outgoing distributions are written into {title}_outgoing.csv,
            with the MT values as the column headers.
        Each of the scattering matrices are written to individual files,
            {title}_scattering_matrix_{mt}_{ell}.csv, with the energy boundaries
            as the row and column headers.

        Parameters
        ----------
        title : string, optional, default is None
            title for the csv files. Default is None, in which case the
            object title attribute will be used (with spaces removed)

        directory : string, optional, default is None
            path of the directory where the files should be written

        verbose : bool, optional, default is False
            If true, will print the files names as they are created

        Returns
        -------
        None

        """

        # create file title
        if title is None:
            stem = f"{self.title.replace(' ','')}_"
        else:
            stem = f"{title}_"

        if directory is not None:
            stem = f"{directory}/{stem}"

        # pointwise
        if hasattr(self, "pointwise"):
            filename = Path(f"{stem}pointwise.csv")

            header = "Energy"
            array = np.array(self.energy_boundaries).reshape(
                (len(self.energy_boundaries), 1)
            )
            for mt in self.pointwise.keys():
                header += f",MT{mt}"
                array = np.hstack(
                    [
                        array,
                        np.append(self.pointwise[mt].values, 0).reshape(
                            (len(self.energy_boundaries), 1)
                        ),
                    ]
                )

            if verbose:
                print(f"\nWriting pointwise data to {filename}")
            np.savetxt(filename, array, delimiter=",", header=header)

        # distributions
        if hasattr(self, "outgoing_distributions"):
            filename = Path(f"{stem}outgoing.csv")

            header = "Energy"
            array = np.array(self.energy_boundaries).reshape(
                (len(self.energy_boundaries), 1)
            )
            for mt in self.outgoing_distributions.keys():
                header += f",MT{mt}"
                array = np.hstack(
                    [
                        array,
                        np.append(self.outgoing_distributions[mt].values, 0).reshape(
                            (len(self.energy_boundaries), 1)
                        ),
                    ]
                )

            if verbose:
                print(f"\nWriting outgoing energy distribution data to {filename}")
            np.savetxt(filename, array, delimiter=",", header=header)

        # scattering matrices
        if hasattr(self, "scattering_matrices"):

            for mt in self.scattering_matrices.keys():

                for ell in range(self.scattering_matrices[mt].number_legendre):

                    filename = Path(f"{stem}scattering_matrix_{mt}_{ell}.csv")
                    array = np.zeros(
                        (
                            len(self.energy_boundaries) + 1,
                            len(self.energy_boundaries) + 1,
                        )
                    )
                    array[1:, 0] = self.energy_boundaries
                    array[0, 1:] = self.energy_boundaries
                    array[1:-1, 1:-1] = self.scattering_matrices[mt].values[:, :, ell]

                    if verbose:
                        print(
                            f"Writing MT{mt} ell={ell} scattering matrix to {filename}"
                        )

                    np.savetxt(filename, array, delimiter=",")
