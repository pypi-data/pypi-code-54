import argparse

from tpy.tmux import execute, execute_prev
from tpy.utils import _HelpAction


def main():
    parser = argparse.ArgumentParser(
        prog="tpy", description="Runs command in tmux", add_help=False
    )
    parser.add_argument("-h", "--help", action=_HelpAction, help="Usage info")
    parser.add_argument(
        "-s", "--session", type=str, default="tpy", help="Session to use"
    )
    parser.add_argument("-w", "--window", type=str, default=None, help="Window to use")
    parser.add_argument(
        "-r",
        "--reset",
        action="store_true",
        help="Resets window before execution, killing running processes",
    )

    subparsers = parser.add_subparsers(dest="task")
    subparsers.required = True

    parser_cmd = subparsers.add_parser(
        "cmd", description="Runs arbitrary command", add_help=False
    )
    parser_cmd.add_argument("command", type=str, help="Command to execute")
    parser_cmd.set_defaults(func=run_cmd)

    parser_cmd_prev = subparsers.add_parser(
        "cmd_prev", description="Runs previous command", add_help=False
    )
    parser_cmd_prev.add_argument(
        "-t",
        "--times_up",
        type=int,
        default=1,
        help="Number of times to press cursor up",
    )
    parser_cmd_prev.set_defaults(func=run_cmd_prev)

    parser_pytest = subparsers.add_parser(
        "pytest", description="Runs pytest on file or directory", add_help=False
    )
    parser_pytest.add_argument("file_or_dir", type=str)
    parser_pytest.add_argument(
        "--executable", type=str, default="pytest", help="pytest executable"
    )
    parser_pytest.add_argument(
        "-k",
        "--keyword",
        type=str,
        default=None,
        help="Only run tests matching given substring expression",
    )
    parser_pytest.add_argument(
        "-m",
        "--mark",
        type=str,
        default=None,
        help="Only run tests matching mark expression",
    )
    parser_pytest.add_argument("--pdb", action="store_true", help="Enables pdb")
    parser_pytest.add_argument("--ipdb", action="store_true", help="Enables ipdb")
    parser_pytest.add_argument(
        "-mf", "--maxfail", type=int, default=None, help="Maximum failures"
    )
    parser_pytest.set_defaults(func=run_pytest)

    parser_python = subparsers.add_parser(
        "python", description="Executes file with python", add_help=False
    )
    parser_python.add_argument("file", type=str)
    parser_python.add_argument(
        "--executable", type=str, default="python", help="Python executable"
    )
    parser_python.add_argument("--pdb", action="store_true", help="Enables pdb")
    parser_python.add_argument("--ipdb", action="store_true", help="Enables ipdb")
    parser_python.add_argument(
        "-i", "--interactive", action="store_true", help="Enables interactive mode"
    )
    parser_python.set_defaults(func=run_python)

    args = parser.parse_args()
    args.func(args)


def run_cmd(args):
    cmd = f"{args.command}"

    execute(cmd, args.session, args.window, args.reset)


def run_cmd_prev(args):
    execute_prev(args.session, args.window, args.reset, args.times_up)


def run_pytest(args):
    assert not (args.pdb and args.ipdb)

    cmd = f"{args.executable} {args.file_or_dir}"

    if args.keyword is not None:
        cmd += f" -k {args.keyword}"
    if args.mark is not None:
        cmd += f" -m {args.mark}"
    if args.maxfail is not None:
        cmd += f" --maxfail={args.maxfail}"
    if args.ipdb:
        cmd += " --pdb --pdbcls=IPython.terminal.debugger:Pdb"
    if args.pdb:
        cmd += " --pdb"

    execute(cmd, args.session, args.window, args.reset)


def run_python(args):
    assert not (args.pdb and args.ipdb)

    cmd = f"{args.executable}"
    if args.interactive:
        cmd += " -i"
    if args.ipdb:
        cmd += " -m ipdb -c continue"
    if args.pdb:
        cmd += " -m pdb -c continue"
    cmd += f" {args.file}"

    execute(cmd, args.session, args.window, args.reset)


if __name__ == "__main__":
    main()
