import os
import shutil

from .common import Config, get_ejudge_contest_dir


def remove_problem(
        ejudge_contest_id: int,
        ejudge_problem_id: int,
        keep_config=False,
) -> None:
    contest_dir = get_ejudge_contest_dir(ejudge_contest_id)
    os.chdir(contest_dir)
    internal_name = None
    config = Config(ejudge_contest_id)
    for i in range(len(config.problems)):
        if config.problems[i]['id'] == ejudge_problem_id:
            internal_name = config.problems[i]['internal_name']
            if not keep_config:
                config.problems.pop(i)
            break
    config.write()
    if internal_name:
        shutil.rmtree(os.path.join(contest_dir, "problems", str(internal_name)))


def remove_contest(
        contest_id: int,
) -> None:
    contest_dir = get_ejudge_contest_dir(contest_id)
    shutil.rmtree(os.path.join(contest_dir, "problems"))
    config = Config(contest_id)
    config.problems.clear()
    config.write()


def add_subparsers(subparsers):
    parser_remove_problem = subparsers.add_parser(
        'rp',
        help="Remove single problem"
    )
    parser_remove_problem.add_argument('contest_id', help='Id of contest in ejudge to remove problem', type=int)
    parser_remove_problem.add_argument('problem_id', help='Problem id in ejudge', type=int)
    parser_remove_problem.set_defaults(
        func=lambda options: remove_problem(options.contest_id, options.problem_id)
    )

    parser_remove_contest = subparsers.add_parser(
        'rc',
        help="Remove all problems from contest"
    )
    parser_remove_contest.add_argument('contest_id', help='Id of contest in ejudge to remove', type=int)
    parser_remove_contest.set_defaults(
        func=lambda options: remove_contest(options.contest_id)
    )
