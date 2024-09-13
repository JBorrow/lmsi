"""
Simple entrypoint
"""

from lmsi.core import core
import argparse as ap
from pathlib import Path

parser = ap.Argumentparser(
    description="Create a webpage from a set of plots."
)

parser.add_argument(
    "--files",
    type=Path,
    nargs="+",
    help="Filenames of the plots to include in the webpage.",
)

parser.add_argument(
    "--config",
    type=Path,
    help="The configuration file to use.",
)

parser.add_argument(
    "--output",
    type=Path,
    help="The output HTML file.",
)

args = parser.parse_args()

def main():
    core(args.files, args.config, args.output)