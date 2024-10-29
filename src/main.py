import argparse
import asyncio
import json
import os
from orientx import config
from orientx.scraper import scrape_x_accounts
from orientx.parser import parse_x_posts
from orientx.classifier import classify_x_posts, load_data, ClassificationPipeline
from orientx.printer import print_driver_df


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Train classifier and scrape, parse, and classify posts!"
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--mode',
        choices=['run', 'train'],
        default='run',
        help='Mode of operation: "run" to scrape and classify (default), "train" to train the model.'
    )
    parser.add_argument(
        '--accounts',
        type=str,
        default='{"Labour": "https://x.com/uklabour?lang=en", "Reform": "https://x.com/reformparty_uk?lang=en"}',
        help='JSON string for user dictionary (default: {"Labour": "https://x.com/uklabour?lang=en", "Reform": "https://x.com/reformparty_uk?lang=en"})'
    )
    parser.add_argument(
        '--num_posts',
        type=int,
        default=10,
        help='Number of posts to scrape per account (default: 10)'
    )
    parser.add_argument(
        '--num_classes',
        type=int,
        default=3,
        help='Number of classification classes (default: 3)'
    )
    parser.add_argument(
        '--model_path',
        type=str,
        default='assets/model.pth',
        help='Path to the model file (default: assets/model.pth)'
    )
    parser.add_argument(
        '--run_output_path',
        type=str,
        default='assets/classified_posts.csv',
        help='Path to save classified posts CSV (default: assets/classified_posts.csv)'
    )
    parser.add_argument(
        '--training_data',
        type=str,
        default='assets/training_dataset.csv',
        help='Path to the training dataset CSV file (required for training mode)'
    )
    parser.add_argument(
        '--num_epochs',
        type=int,
        default=10,
        help='Number of epochs for training (default: 10)'
    )
    parser.add_argument(
        '--train_output_path',
        type=str,
        default='assets/model.pth',
        help='Path to save the trained model (default: assets/model.pth)'
    )
    parser.add_argument(
        '--max_length',
        type=int,
        default=128,
        help='Maximum sequence length (default: 128)'
    )
    parser.add_argument(
        '--batch_size',
        type=int,
        default=16,
        help='Batch size for training (default: 16)'
    )
    parser.add_argument(
        '--learning_rate',
        type=float,
        default=2e-5,
        help='Learning rate (default: 2e-5)'
    )

    return parser.parse_args()


def validate_arguments(args):
    if not (isinstance(args.num_posts, int) and args.num_posts >= 1):
        raise ValueError("num_posts must be an integer greater than or equal to 1.")

    if not (isinstance(args.num_classes, int) and args.num_classes >= 1):
        raise ValueError("num_classes must be an integer greater than or equal to 1.")

    if not os.path.isfile(args.model_path):
        raise ValueError(f"model_path '{args.model_path}' must be a valid file path.")

    if not os.path.isdir(os.path.dirname(args.run_output_path)):
        raise ValueError(f"run_output_path '{args.run_output_path}' must be a valid directory path.")

    if args.mode == 'train' and not os.path.isfile(args.training_data):
        raise ValueError(f"training_data '{args.training_data}' must be a valid file path.")

    if not (isinstance(args.num_epochs, int) and args.num_epochs >= 1):
        raise ValueError("num_epochs must be an integer greater than or equal to 1.")

    if not os.path.isdir(os.path.dirname(args.train_output_path)):
        raise ValueError(f"train_output_path '{args.train_output_path}' must be a valid directory path.")

    if not (isinstance(args.max_length, int) and args.max_length >= 1):
        raise ValueError("max_length must be an integer greater than or equal to 1.")

    if not (isinstance(args.batch_size, int) and args.batch_size >= 1):
        raise ValueError("batch_size must be an integer greater than or equal to 1.")

    if not (isinstance(args.learning_rate, float) and args.learning_rate >= 0):
        raise ValueError("learning_rate must be a non-negative float.")


def run_orientx(args):
    accounts_dict = json.loads(args.accounts)

    pipeline = ClassificationPipeline(model_name='bert-base-uncased', num_classes=args.num_classes)
    pipeline.load_model(args.model_path)

    async def async_main():
        scraped_data = await scrape_x_accounts(accounts_dict, num_posts=args.num_posts)
        parsed_df = parse_x_posts(scraped_data)
        classifications_df = classify_x_posts(pipeline, parsed_df)
        classifications_df.to_csv(args.run_output_path, index=False)

        #print_driver_df("Classified Posts", classifications_df)
        filtered_df = classifications_df[classifications_df['pinned'] == True]

        # Print the filtered DataFrame
        print(filtered_df)

    asyncio.run(async_main())


def train_orientx(args):
    (train_texts, train_labels), (val_texts, val_labels) = load_data(args.training_data)

    pipeline = ClassificationPipeline(
        model_name='bert-base-uncased',
        num_classes=args.num_classes,
        max_length=args.max_length,
        batch_size=args.batch_size,
        lr=args.learning_rate,
        epochs=args.num_epochs
    )

    pipeline.prepare_data(train_texts, train_labels, val_texts, val_labels)
    pipeline.train(args.train_output_path)


def main():
    args = parse_arguments()
    config.VERBOSE = args.verbose

    validate_arguments(args)

    if args.mode == 'train':
        train_orientx(args)
    else:
        run_orientx(args)


if __name__ == "__main__":
    main()
