import pandas as pd

from orientx import config
from orientx.arguments import create_parser, validate_arguments
from orientx.printer import print_parameters
from .simple_analyses import analyze_posts_data


def main():
    parser = create_parser(module_name='analyzer')
    args = parser.parse_args()
    validate_arguments(args)

    config.QUIET = args.quiet
    print_parameters(args)

    classified_df = pd.read_csv(args.input_path)

    analyze_posts_data(classified_df)


if __name__ == "__main__":
    main()
