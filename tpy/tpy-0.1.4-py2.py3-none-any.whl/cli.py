import argparse

from tpy.tmux import execute, execute_prev
from tpy.utils import _HelpAction


def main():
    # fmt: off
    parser = argparse.ArgumentParser(
        prog="tpy", 
        description="Runs command in tmux", 
        add_help=False
    )
    parser.add_argument(
        "--session", 
        type=str, 
        default="tpy", 
        help="Session to use"
    )
    parser.add_argument(
        "--window", 
        type=str, 
        default=None, 
        help="Window to use"
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Resets window before execution, killing running processes",
    )
    parser.add_argument(
        "-h", "--help", 
        action=_HelpAction, 
        help="Usage info"
    )

    subparsers = parser.add_subparsers(dest="task")
    subparsers.required = True

    parser_cmd = subparsers.add_parser(
        "cmd", 
        description="Runs arbitrary command", 
        add_help=False
    )
    parser_cmd.add_argument(
        "command", 
        type=str, 
        help="Command to execute"
    )
    parser_cmd.set_defaults(func=run_cmd)

    parser_cmd_prev = subparsers.add_parser(
        "cmd_prev", 
        description="Runs previous command", 
        add_help=False
    )
    parser_cmd_prev.add_argument(
        "-cu",
        "--cursor_up",
        type=int,
        default=1,
        help="Number of times to press cursor up",
    )
    parser_cmd_prev.set_defaults(func=run_cmd_prev)

    parser_pytest = subparsers.add_parser(
        "pytest", 
        description="Runs pytest on file or directory. Any additional arguments are passed on.", 
        add_help=False
    )
    parser_pytest.add_argument(
        "file_or_dir", 
        type=str
    )
    parser_pytest.add_argument(
        "-e", "--executable", 
        type=str, 
        default="pytest", 
        help="pytest executable"
    )
    parser_pytest.add_argument(
        "--ipdb", 
        action="store_true", 
        help="Enables ipdb"
    )
    parser_pytest.set_defaults(func=run_pytest)

    parser_python = subparsers.add_parser(
        "python", 
        description="Executes file with python. Any additional arguments are passed on.", 
        add_help=False
    )
    parser_python.add_argument(
        "file", 
        type=str
    )
    parser_python.add_argument(
        "-e", "--executable", 
        type=str, 
        default="python", 
        help="Python executable"
    )
    parser_python.add_argument(
        "--pdb", 
        action="store_true", 
        help="Enables pdb"
    )
    parser_python.add_argument(
        "--ipdb", 
        action="store_true", 
        help="Enables ipdb"
    )
    parser_python.set_defaults(func=run_python)

    # fmt: on
    args, unknownargs = parser.parse_known_args()
    args.unknownargs = unknownargs
    args.func(args)


def run_cmd(args):
    cmd = f"{args.command}"

    execute(cmd, args.session, args.window, args.reset)


def run_cmd_prev(args):
    execute_prev(args.session, args.window, args.reset, args.cursor_up)


def run_pytest(args):
    cmd = f"{args.executable} {args.file_or_dir}"
    cmd += f" {' '.join(args.unknownargs)}"
    
    if args.ipdb:
        cmd += " --pdb --pdbcls=IPython.terminal.debugger:Pdb"

    execute(cmd, args.session, args.window, args.reset)


def run_python(args):
    assert not (args.pdb and args.ipdb)

    cmd = f"{args.executable}"
    cmd += f" {' '.join(args.unknownargs)}"

    if args.ipdb:
        cmd += " -m ipdb -c continue"
    if args.pdb:
        cmd += " -m pdb -c continue"
    cmd += f" {args.file}"

    execute(cmd, args.session, args.window, args.reset)


if __name__ == "__main__":
    main()
