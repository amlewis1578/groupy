import argparse
import sys
import ENDFtk
from pathlib import Path
from groupy import run_njoy, GrouprOutput


def main(argv=sys.argv[1:]):

    parser = argparse.ArgumentParser()
    parser.add_argument("endf_file", type=str, help="Path to ENDF6-formatted file")
    parser.add_argument("--temp", type=float, help="Temperature in K", default=293)
    parser.add_argument("--groups", type=int, help="Grouping option", default=2)
    parser.add_argument(
        "--flux",
        type=int,
        help="Weighting flux option",
        default=5,
        choices=[2, 3, 5, 9, 11],
    )
    parser.add_argument("-v", action="store_true", help="Verbose mode")

    args = parser.parse_args(argv)

    verbose = args.v
    if verbose:
        print(f"Running for: {args.endf_file}")
        print(f"  At temperature {args.temp} K")
        print(f"  With group option {args.groups}")
        print(f"  with flux option {args.flux}")

    # check file, and create title
    endf_file = Path(args.endf_file)
    if not endf_file.exists():
        raise FileNotFoundError(f"Cannot find ENDF6 file {endf_file}")

    tape = ENDFtk.tree.Tape.from_file(str(endf_file))
    mat_num = tape.material_numbers[0]
    mat = tape.material(mat_num)
    file1 = mat.file(1).parse()
    desc = file1.section(451).description
    isotope = desc.splitlines()[0][:11].replace(" ", "")
    isotope = "".join(isotope.split("-")[1:])
    title = f"grouped{isotope}"

    run_njoy(
        endf_file,
        title,
        temperature=args.temp,
        group_boundaries=args.groups,
        flux=args.flux,
        verbose=verbose,
    )

    # collect the output
    gendf_file = "tape91"
    if verbose:
        print(f"\nParsing GROUPR output...")

    print("\n(ENDFtk info messages can be ignored)")
    obj = GrouprOutput(gendf_file)

    if verbose:
        print(f"\nWriting out to csv files....")
    # write the output files
    obj.write_to_csv()

    if verbose:
        print("\nFinished")
