import os
import shutil

from .common import Config, get_ejudge_contest_dir
from .config import SOLUTION_FOLDER_NAMES
from .login import EjudgeAuthSession


def submit_problem(
        ejudge_contest_id: int,
        ejudge_problem_id: int,
        only_main_correct=False,
        no_lint=False,
) -> None:
    contest_dir = get_ejudge_contest_dir(ejudge_contest_id)
    os.chdir(contest_dir)

    internal_name = None
    id = None

    config = Config(ejudge_contest_id)
    for i in range(len(config.problems)):
        if 'id' in config.problems[i] and config.problems[i]['id'] == ejudge_problem_id:
            internal_name = config.problems[i]['internal_name']
            id = i

    if id is None:
        return

    problem_path = os.path.join(contest_dir, "problems", str(internal_name))

    session = EjudgeAuthSession(ejudge_contest_id)

    if 'solution_cmd' in config.problems[id]:
        solution_prefix = config.problems[id]['solution_cmd']
        files = os.listdir(problem_path)
        for file in files:
            if file.startswith(solution_prefix):
                session.submit_file(os.path.join(problem_path, file), ejudge_problem_id, no_lint)

    if only_main_correct:
        return

    for solution_folder_name in SOLUTION_FOLDER_NAMES:
        folder_path = os.path.join(problem_path, solution_folder_name)
        if os.path.exists(folder_path):
            files = os.listdir(folder_path)
            for file in files:
                session.submit_file(os.path.join(folder_path, file), ejudge_problem_id, no_lint)

    print("Submitted problem ", ejudge_problem_id)


def submit_contest(
        contest_id: int,
        only_main_correct=False,
        no_lint=False,
) -> None:
    config = Config(contest_id)
    for problem in config.problems:
        if "abstract" not in problem:
            submit_problem(contest_id, problem['id'], only_main_correct, no_lint)


def add_subparsers(subparsers):
    parser_submit_problem = subparsers.add_parser(
        'sp',
        help="Submit solutions for single problem"
    )

    parser_submit_problem.add_argument('contest_id', help='Id of ejudge contest to submit solutions', type=int)
    parser_submit_problem.add_argument('problem_id', help='Id of problem in contest to submit solutions', type=int)
    parser_submit_problem.add_argument('-m', "--only-main", help="Submit only main correct solution", action="store_true")
    parser_submit_problem.add_argument('-n', "--no-lint", help="Modify solutions to be ignored by linter", action="store_true")
    parser_submit_problem.set_defaults(
        func=lambda options: submit_problem(options.contest_id, options.problem_id, options.only_main, options.no_lint)
    )

    parser_submit_contest = subparsers.add_parser(
        'sc',
        help="Submit solutions for all problems in contest"
    )
    parser_submit_contest.add_argument('contest_id', help='Id of contest in ejudge to submit solutions', type=int)
    parser_submit_contest.add_argument('-m', "--only-main", help="Submit only main correct solution", action="store_true")
    parser_submit_contest.add_argument('-n', "--no-lint", help="Modify solutions to be ignored by linter", action="store_true")
    parser_submit_contest.set_defaults(
        func=lambda options: submit_contest(options.contest_id, options.only_main, options.no_lint)
    )
