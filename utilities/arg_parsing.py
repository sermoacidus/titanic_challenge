"""Use the module to parse user-input arguments:
path to files, threads needed to run scripts concurrently
"""
import argparse


def args_parse(args):
    """
    Used to set the arguments for the app. Run it from console:
    python main.py -p path to csv.files [addition path ...] -t [amount of threads to run with]
    """
    parser = argparse.ArgumentParser(
        description="Parser for files' path and threads amount"
    )
    parser.add_argument(
        "-p", "--path", nargs="+", help='set the path to the folder with "*.csv" files'
    )
    parser.add_argument(
        "-t",
        "--threads",
        nargs="?",
        const="threads",
        default=1,
        help="set the number of threads for the script",
        type=int,
    )
    return parser.parse_args(args)
