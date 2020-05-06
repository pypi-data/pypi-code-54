from sys import stderr

from ftests.cli_args import CliArgs
from ftests.tests_definition import TestsDefinition


def main():
    try:
        args = CliArgs.get_cli_args()
        tests_definition_file = TestsDefinition(args.get_file_full_path())
        print('Tests results:')
        tests_results = tests_definition_file.launch_tests()
        print(f'\n{len(tests_results)} test{"" if len(tests_results) == 1 else "s"} run.')

        are_all_tests_passed = all([result.is_passed() for result in tests_results])
        exit(0 if are_all_tests_passed else 1)
    except Exception as e:
        print(e, file=stderr)
        exit(3)


if __name__ == '__main__':
    main()
