import asyncio
import json

from orientx import config
from orientx.arguments import create_parser, validate_arguments
from orientx.printer import print_parameters
from .scraper import scrape_multiple_accounts


async def async_main():
    parser = create_parser(module_name='scraper')
    args = parser.parse_args()
    validate_arguments(args, 'scraper')

    config.QUIET = args.quiet
    print_parameters(args)

    accounts_dict = json.loads(args.accounts)
    scraped_data = await scrape_multiple_accounts(accounts_dict, num_posts=args.num_posts, batch_size=args.scrape_batch_size)

    with open(args.output_path, 'w') as json_file:
        json.dump(scraped_data, json_file, indent=4)


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
