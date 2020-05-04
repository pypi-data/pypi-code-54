import sys
import os
import argparse

from sequana.pipelines_common import *
from sequana.snaketools import Module
from sequana import logger
logger.level = "INFO"

col = Colors()

NAME = "multitax"
m = Module(NAME)
m.is_executable()


class Options(argparse.ArgumentParser):
    def __init__(self, prog=NAME, epilog=None):
        usage = col.purple(sequana_prolog.format(**{"name": NAME}))
        super(Options, self).__init__(usage=usage, prog=prog, description="",
            epilog=epilog,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

        # add a new group of options to the parser
        so = SlurmOptions()
        so.add_options(self)

        # add a snakemake group of options to the parser
        so = SnakemakeOptions(working_directory=NAME)
        so.add_options(self)

        so = InputOptions()
        so.add_options(self)

        so = GeneralOptions()
        so.add_options(self)

        pipeline_group = self.add_argument_group("pipeline")

        pipeline_group.add_argument('--kraken-level', dest="kraken_level",
            default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        pipeline_group.add_argument("--databases", dest="databases", type=str,
            nargs="+",
            help="""Path to a valid Kraken database(s). See sequana_taxonomy
                standaline to download some. You may use several, in which case, an
                iterative taxonomy is performed as explained in online sequana
                documentation.""")



def main(args=None):

    if args is None:
        args = sys.argv

    # whatever needs to be called by all pipeline before the options parsing
    init_pipeline(NAME)

    # option parsing including common epilog
    options = Options(NAME, epilog=sequana_epilog).parse_args(args[1:])

    # the real stuff is here
    manager = PipelineManager(options, NAME)

    # create the beginning of the command and the working directory
    manager.setup()

    # fill the config file with input parameters
    cfg = manager.config.config
    cfg.input_directory = os.path.abspath(options.input_directory)
    cfg.input_pattern = options.input_pattern
    cfg.input_readtag = options.input_readtag

    cfg['sequana_taxonomy']['level'] = options.kraken_level
    cfg['sequana_taxonomy']['databases'] = options.databases

    # finalise the command and save it; copy the snakemake. update the config
    # file and save it.
    manager.teardown()


if __name__ == "__main__":
    main()
