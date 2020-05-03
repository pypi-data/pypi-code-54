import os

from cliff.command import Command

from enough import settings
from enough.common.openstack import OpenStack


def set_common_options(parser):
    parser.add_argument(
        '--clouds',
        default=os.environ.get('OS_CLIENT_CONFIG_FILE',
                               f'{settings.CONFIG_DIR}/inventory/group_vars/all/clouds.yml'),
        help='Path to the clouds.yml file')
    return parser


class Cli(Command):
    "OpenStack client"

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('args', nargs='+')
        return set_common_options(parser)

    def take_action(self, parsed_args):
        args = vars(self.app.options)
        args.update(vars(parsed_args))
        o = OpenStack(settings.CONFIG_DIR, args['clouds'])
        o.run(args['args'])
