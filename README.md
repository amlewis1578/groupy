# `groupy`

package to parse GENDF files, which are the output of the [NJOY](https://github.com/njoy/NJOY2016) GROUPR module. 



## dependencies

The LANL program [NJOY](https://github.com/njoy/NJOY2016) must be installed, and the executable should be available on the path.  **Running NJOY with `groupy` has currently only been tested on Ubuntu 22.04**. 

This package requires that the LANL program [ENDFtk](https://github.com/njoy/ENDFtk) is installed and added to the python path.

## installation

Move into the `groupy` directory and run

```bash
pip install .
```

## using the `groupy` package

The main function is the `get_grouped_data` function.

```python
from groupy import get_grouped_data

obj = get_grouped_data("<endf6-file>", title)
```

`get_grouped_data` has many optional parameters to customize the NJOY input.

```
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

```

### Running NJOY

NJOY can be run individually with the `run_njoy` function.

```python
from groupy import run_njoy

run_njoy("<endf6-file>", title)
```

`run_njoy` has many optional parameters to customize the NJOY input.

```
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

    flux : int, optional, default is 5
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
```

The group boundary and flux options are explained in detail in the [NJOY Manual](https://github.com/njoy/NJOY2016-manual).

The `GROUPR` output is put into a file named `tape91`. 


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

## Command Line Interface

There is a command line interface to the `get_grouped_data` function with limited options. It can be called with 

```bash
group <endf6-file>
```

The optional flags are: 

```bash
usage: group [-h] [--temp TEMP] [--groups GROUPS] [--flux {2,3,5,9,11}] [-v] endf_file

positional arguments:
  endf_file            Path to ENDF6-formatted file

options:
  -h, --help           show this help message and exit
  --temp TEMP          Temperature in K
  --groups GROUPS      Grouping option
  --flux {2,3,5,9,11}  Weighting flux option
  -v                   Verbose mode
```

The CLI does not allow for a list of group boundaries, only the integer grouping options.
It also does not allow for the default tolerance values or legendre order to be changed, and automatically creates the title "groupedAAAXX"