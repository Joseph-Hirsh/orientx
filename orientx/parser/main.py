import asyncio
import json

from orientx import config
from orientx.arguments import create_parser, validate_arguments
from orientx.printer import print_parameters
from .posts_parser import parse_x_posts


def main():
    parser = create_parser(module_name='parser')
    args = parser.parse_args()
    validate_arguments(args)

    config.QUIET = args.quiet
    print_parameters(args)

    with open(args.input_path, 'r') as json_file:
        scraped_posts = json.load(json_file)

    parsed_tweets_df = parse_x_posts(scraped_posts)
    parsed_tweets_df.to_csv(args.output_path)


if __name__ == "__main__":
    main()
