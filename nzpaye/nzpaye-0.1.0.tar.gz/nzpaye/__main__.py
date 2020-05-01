from nzpaye.main import paye_summary
from nzpaye import argument_parser


def main():
    parser = argument_parser.get_parser()
    options = parser.parse_args()
    paye_summary(options)

if __name__ == "__main__":
    main()