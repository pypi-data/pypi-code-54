import argparse

from tpy.tmux import execute, execute_prev
from tpy.utils import _HelpAction


def main():
    # fmt: off
    parser = argparse.ArgumentParser(
        prog="tpy", 
        description="Runs commands in tmux.", 
        add_help=False
    )
    parser.add_argument(
        "--session", 
        type=str, 
        default="tpy", 
        help="Name of session to use"
    )
    parser.add_argument(
        "--window", 
        type=str, 
        default=None, 
        help="Name of window to use"
    )
    parser.add_argument(
        "--reset-window",
        action="store_true",
        help="Resets window before execution",
    )
    parser.add_argument(
        "--reset-pane",
        action="store_true",
        help="Resets pane before execution",
    )
    parser.add_argument(
        "--dry",
        action="store_true",
        help="Will send but not execute commands",
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
        description="Runs arbitrary command.", 
        add_help=False
    )
    parser_cmd.add_argument(
        "command", 
        type=str, 
        help="Command to execute"
    )
    parser_cmd.set_defaults(func=run_cmd)

    parser_again = subparsers.add_parser(
        "again", 
        description="Runs previous command again.", 
        add_help=False
    )
    parser_again.add_argument(
        "-tu",
        "--times-up",
        type=int,
        default=1,
        help="Number of times to press cursor up",
    )
    parser_again.set_defaults(func=run_cmd_prev)
    # fmt: on

    args, unknownargs = parser.parse_known_args()
    args.unknownargs = unknownargs
    args.func(args)


def run_cmd(args):
    cmd = f"{args.command}"
    execute(
        cmd,
        args.session,
        args.window,
        None,
        args.reset_window,
        args.reset_pane,
        args.dry,
    )


def run_cmd_prev(args):
    execute_prev(
        args.session,
        args.window,
        None,
        args.reset_window,
        args.reset_pane,
        args.times_up,
        args.dry,
    )


if __name__ == "__main__":
    main()
