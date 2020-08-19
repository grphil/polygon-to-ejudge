#!/usr/bin/env python3

import argparse
from sys import argv

from . import import_problem
from . import remove_problem
from . import update_problem
from . import login

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(
        title='available subcommands',
        description='',
        help='DESCRIPTION',
        metavar="SUBCOMMAND",
)

subparsers.required = True

import_problem.add_subparsers(subparsers)
remove_problem.add_subparsers(subparsers)
update_problem.add_subparsers(subparsers)
login.add_subparsers(subparsers)


def main():
    options = parser.parse_args(argv[1:])
    options.func(options)


if __name__ == "__main__":
    main()