import os
import sys
import subprocess as sp
from typing import Optional

import click
from click_help_colors import HelpColorsCommand

CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    max_content_width=120,
)
DEFAULT_COLOR_OPTIONS = dict(
    help_headers_color='white',
    help_options_color='cyan',
)


def get_line_count(filepath: str) -> int:
    with open(filepath) as f:
        lines = f.readlines()
    return len(lines)


def get_line(filepath: str, n: int) -> Optional[str]:
    with open(filepath) as f:
        for i, line in enumerate(f):
            if i+1 == n:
                return line.rstrip()
    return None


@click.command(
    cls=HelpColorsCommand,
    context_settings=CONTEXT_SETTINGS,
    **DEFAULT_COLOR_OPTIONS,  # type: ignore
)
@click.argument('task_list_file_path', nargs=1)
@click.option(
    '-m', '--mem', type=int, default=5,
    help='Total memory requirement (GB).',
)
@click.option(
    '-t', '--threads', type=int, default=1,
    help='Thu number of threads requirement.',
)
@click.option(
    '-n', '--name', type=str, default='array_job_task',
    help='Name of job',
)
def run_tasks(
    task_list_file_path: str,
    mem: int,
    threads: int,
    name: str,
) -> None:
    """
    Run lines of `task_list_file_path` as a array job,
    where a single job is corresponding to one line.
    """
    cmd_str = (
        f'qsub -cwd '
        f'-l mem_req={mem/threads}G,s_vmem={mem/threads}G '
        f'-pe def_slot {threads} '
        f'-o $(pwd)/qlog -e $(pwd)/qlog '
        f'-N {name} '
        f'-t 1-{get_line_count(task_list_file_path)} '
        f'array_job_task_runner {task_list_file_path}'
    )
    output = sp.run(
        cmd_str,
        shell=True,
        stdout=sp.PIPE,
    ).stdout.decode('utf-8')
    print(output)


CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    max_content_width=120,
)
DEFAULT_COLOR_OPTIONS = dict(
    help_headers_color='white',
    help_options_color='cyan',
)


@click.command(
    cls=HelpColorsCommand,
    context_settings=CONTEXT_SETTINGS,
    **DEFAULT_COLOR_OPTIONS,  # type: ignore
)
@click.argument('task_list_file_path', nargs=1)
def array_job_task_runner(
    task_list_file_path: str,
) -> None:
    try:
        sge_task_id = int(os.environ['SGE_TASK_ID'])
    except Exception:
        print('failed to fetch SGE_TASK_ID', file=sys.stderr)
        sys.exit(1)

    task = get_line(task_list_file_path, sge_task_id)
    if task is None:
        print('failed to get task from {} by SGE_TASK_ID: {}'.format(
            task_list_file_path,
            sge_task_id,
        ), file=sys.stderr)
        sys.exit(1)
    sp.run(
        task,
        shell=True,
    )
