#!/usr/bin/env python3

import argparse
from sys import argv

from polygon_to_ejudge import import_problem
from polygon_to_ejudge import remove_problem
from polygon_to_ejudge import update_problem
from polygon_to_ejudge import login

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