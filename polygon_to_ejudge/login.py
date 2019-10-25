import os

import polygon_cli.config


def logout():
    # TODO: chose login
    os.remove(polygon_cli.config.authentication_file)
    polygon_cli.config.login = None


def add_subparsers(subparsers):
    parser_logout = subparsers.add_parser(
        'logout',
        help="Log out of your login in ejudge"
    )
    parser_logout.set_defaults(func=lambda options: logout())
