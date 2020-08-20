import os

from .common import get_ejudge_contest_dir, Config
from .import_problem import import_problem
from .remove_problem import remove_problem


def update_problem(
        ejudge_contest_id: int,
        ejudge_problem_id: int,
) -> None:
    contest_dir = get_ejudge_contest_dir(ejudge_contest_id)
    os.chdir(contest_dir)
    config = Config(ejudge_contest_id)

    polygon_id = None

    short_name = None

    for problem in config.problems:
        if 'id' in problem and problem["id"] == ejudge_problem_id:
            if "extid" in problem:
                polygon_id = problem["extid"]
                polygon_id = int(polygon_id[polygon_id.find(":") + 1:])
                if "short_name" in problem:
                    short_name = problem["short_name"]

    if not polygon_id:
        raise Exception("No polygon id found, can not update")

    remove_problem(ejudge_contest_id, ejudge_problem_id, keep_config=True)
    import_problem(ejudge_contest_id, polygon_id, short_name, ejudge_problem_id)


def update_contest(
        contest_id: int,
) -> None:
    config = Config(contest_id)
    for problem in config.problems:
        if 'extid' in problem:
            if problem['extid'].startswith('polygon'):
                update_problem(contest_id, problem['id'])


def add_subparsers(subparsers):
    parser_update_problem = subparsers.add_parser(
        'up',
        help="Update single problem"
    )
    parser_update_problem.add_argument('contest_id', help='Id of contest in ejudge', type=int)
    parser_update_problem.add_argument('problem_id', help='Problem id in ejudge', type=int)
    parser_update_problem.set_defaults(
        func=lambda options: update_problem(options.contest_id, options.problem_id)
    )

    parser_update_contest = subparsers.add_parser(
        'uc',
        help="Update each problem in ejudge contest"
    )
    parser_update_contest.add_argument('contest_id', help='Ejudge contest id', type=int)
    parser_update_contest.set_defaults(
        func=lambda options: update_contest(options.contest_id)
    )
