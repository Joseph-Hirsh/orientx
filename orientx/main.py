# orientx.main.py
import json
import asyncio

from orientx import config
from orientx.arguments import create_parser, validate_arguments
from orientx.analyzer import analyze_posts_data
from orientx.printer import print_driver_df, print_parameters
from orientx.scraper import scrape_x_accounts
from orientx.parser import parse_x_posts
from orientx.classifier import classify_x_posts, load_data, ClassificationPipeline


def run_orientx(args):
    accounts_dict = json.loads(args.accounts)

    pipeline = ClassificationPipeline(model_name='bert-base-uncased', num_classes=args.num_classes)
    pipeline.load_model(args.model_path)

    async def async_main():
        scraped_data = await scrape_x_accounts(accounts_dict, num_posts=args.num_posts,
                                               batch_size=args.scrape_batch_size, scroll_mode=args.scroll_mode)
        parsed_df = parse_x_posts(scraped_data)
        classifications_df = classify_x_posts(pipeline, parsed_df)

        classifications_df.to_csv(args.output_path, index=False)
        print_driver_df("Classified Posts", classifications_df)

        analyze_posts_data(classifications_df)

    asyncio.run(async_main())


def train_orientx(args):
    (train_texts, train_labels), (val_texts, val_labels) = load_data(args.training_data)

    pipeline = ClassificationPipeline(
        model_name='bert-base-uncased',
        num_classes=args.num_classes,
        max_length=args.max_input_length,
        batch_size=args.train_batch_size,
        lr=args.learning_rate,
        epochs=args.num_epochs
    )

    pipeline.prepare_data(train_texts, train_labels, val_texts, val_labels)
    pipeline.train(args.train_output_path)


def main():
    parser = create_parser('main')
    args = parser.parse_args()
    validate_arguments(args, 'main')

    config.QUIET = args.quiet
    print_parameters(args)

    if args.mode == 'train':
        train_orientx(args)
    else:
        run_orientx(args)


if __name__ == "__main__":
    main()
