# `groupy`

package to parse GENDF files, which are the output of the [NJOY](https://github.com/njoy/NJOY2016) GROUPR module. 

## installation

This package requires the LANL program [ENDFtk](https://github.com/njoy/ENDFtk).

move into the `groupy` directory and run

```bash
pip install .
```

## using the `groupy` package

### Parsing a GENDF file

The output of the `GROUPR` module is a GENDF-formatted file. The `GrouprOutput` class can currently parse the energy boundaries (MF1), pointwise values (MF3), outgoing energy distributions (MF5) and scattering matrices (MF6) from the GENDF-formatted file.

```python
from groupy import GrouprOutput

obj = GrouprOutput(<gendf-file>)
```

The energy group boundaries, in eV, are in `obj.energy_boundaries`. 

The pointwise values are in the dictionary `obj.pointwise`, which has MT values for keys and `PointwiseValues` objects as values. The values can be accessed with `obj.pointwise[mt].values`.

Outgoing energy distributions are in the dictionary `obj.outgoing_distributions`, and the scattering matrices are in the dictionary `obj.scattering_matrices`. The values are accessed and plotted in an [example file](docs/parse_gendf.ipynb).

The values can be written out to CSV files with the `obj.write_to_csv()` function.