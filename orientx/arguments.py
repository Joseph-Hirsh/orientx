import argparse
import os
import json

from orientx.printer import print_argument_error


def validate_arguments(args, module_name):
    def check_and_convert_path(attr):
        if hasattr(args, attr):
            setattr(args, attr, os.path.abspath(getattr(args, attr)))

    for path_attr in ['output_path', 'input_path', 'model_path', 'train_output_path', 'training_data']:
        check_and_convert_path(path_attr)

    if hasattr(args, 'accounts'):
        try:
            json.loads(args.accounts)
        except json.JSONDecodeError:
            print_argument_error(f"Invalid JSON string for accounts: {args.accounts}")
            exit()

    for attr in ['num_posts', 'scrape_batch_size', 'train_batch_size', 'num_epochs']:
        if hasattr(args, attr) and getattr(args, attr) < 1:
            print_argument_error(f"{attr} must be an integer greater than or equal to 1, got {getattr(args, attr)}")
            exit()

    if hasattr(args, 'scroll_mode') and args.scroll_mode not in ['manual', 'auto']:
        print_argument_error(f"scroll_mode must be 'manual' or 'auto', got {args.scroll_mode}")
        exit()

    if hasattr(args, 'output_path'):
        classifier_output_dir = os.path.dirname(args.output_path)
        if not os.path.exists(classifier_output_dir):
            print_argument_error(f"Output path directory does not exist for classifier: {classifier_output_dir}")
            exit()

    if hasattr(args, 'input_path'):
        if module_name in ['classifier', 'analyzer']:
            if (hasattr(args, 'mode') and args.mode == 'inference') and not (os.path.isfile(args.input_path) and args.input_path.endswith('.csv')):
                print_argument_error(
                    f"input_path must be a valid existing .csv file for {module_name}, got {args.input_path}")
                exit()
        elif module_name == 'parser':
            if not (os.path.isfile(args.input_path) and args.input_path.endswith('.json')):
                print_argument_error(
                    f"input_path must be a valid existing .json file for {module_name}, got {args.input_path}")
                exit()

    if hasattr(args, 'mode') and args.mode not in ['inference', 'train']:
        print_argument_error(f"mode must be 'inference' or 'train', got {args.mode}")
        exit()

    if hasattr(args, 'num_classes') and args.num_classes < 2:
        print_argument_error(f"num_classes must be an integer greater than or equal to 2, got {args.num_classes}")
        exit()

    if hasattr(args, 'model_path'):
        if (hasattr(args, 'mode') and args.mode == 'inference') and not (args.model_path.endswith('.pth') and os.path.isfile(args.model_path)):
            print_argument_error(f"model_path must be a valid path to a .pth file, got {args.model_path}")
            exit()

    if hasattr(args, 'learning_rate') and args.learning_rate <= 0:
        print_argument_error(f"learning_rate must be a float greater than 0, got {args.learning_rate}")
        exit()

    if hasattr(args, 'max_input_length') and args.max_input_length < 1:
        print_argument_error(
            f"max_input_length must be an integer greater than or equal to 1, got {args.max_input_length}")
        exit()

    if hasattr(args, 'test_size') and not (0 < args.test_size < 1):
        print_argument_error(f"test_size must be a float between 0 and 1, got {args.test_size}")
        exit()

    if hasattr(args, 'train_output_path'):
        train_output_dir = os.path.dirname(args.train_output_path)
        if not os.path.exists(train_output_dir):
            print_argument_error(f"train_output_path directory does not exist: {train_output_dir}")
            exit()

    if hasattr(args, 'training_data') and (
            not os.path.isfile(args.training_data) or not args.training_data.endswith('.csv')):
        print_argument_error(f"training_data must be a valid path to an existing .csv file, got {args.training_data}")
        exit()

    if hasattr(args, 'output_path'):
        classifier_output_dir = os.path.dirname(args.output_path)
        if not os.path.exists(classifier_output_dir):
            print_argument_error(f"Output path directory does not exist for classifier: {classifier_output_dir}")
            exit()


def add_scraper_arguments(argument_parser, individual=True):
    argument_parser.add_argument(
        '--accounts',
        type=str,
        default='{"Labour": "https://x.com/uklabour?lang=en", "Reform": "https://x.com/reformparty_uk?lang=en", "UKIP": "https://x.com/ukip?lang=en"}',
        help='JSON string for user dictionary (default: {"Labour": "https://x.com/uklabour?lang=en", "Reform": "https://x.com/reformparty_uk?lang=en", "UKIP": "https://x.com/ukip?lang=en"})'
    )
    argument_parser.add_argument(
        '--num_posts',
        type=int,
        default=10,
        help='Number of posts to scrape per account (default: 10)'
    )
    argument_parser.add_argument(
        '--scrape_batch_size',
        type=int,
        default=2,
        help='Batch size for scraping accounts in parallel (default: 2)'
    )
    argument_parser.add_argument(
        '--scroll_mode',
        choices=['manual', 'auto'],
        default='auto',
        help='Scrape with manual scrolling or automatic scrolling'
    )

    if individual:
        argument_parser.add_argument(
            '--output_path',
            type=str,
            default="assets/scraped_posts.json",
            help='Output path for scraped posts (default: assets/scraped_posts.json)'
        )


def add_parser_arguments(argument_parser, individual=True):
    if individual:
        argument_parser.add_argument(
            '--input_path',
            type=str,
            default="assets/scraped_posts.json",
            help='Path to scraped posts (default: assets/scraped_posts.json)'
        )
        argument_parser.add_argument(
            '--output_path',
            type=str,
            default="assets/parsed_posts.csv",
            help='Output path for parsed posts (default: assets/parsed_posts.csv)'
        )


def add_classifier_arguments(argument_parser, individual=True):
    argument_parser.add_argument(
        '--mode',
        choices=['inference', 'train'],
        default='inference',
        help='Mode of operation: "inference" to scrape and classify (default), "train" to train the model.'
    )
    argument_parser.add_argument(
        '--num_classes',
        type=int,
        default=3,
        help='Number of classification classes (default: 3)'
    )
    argument_parser.add_argument(
        '--model_path',
        type=str,
        default='assets/model.pth',
        help='Path to the model file (default: assets/model.pth)'
    )
    argument_parser.add_argument(
        '--learning_rate',
        type=float,
        default=2e-5,
        help='Learning rate (default: 2e-5)'
    )
    argument_parser.add_argument(
        '--max_input_length',
        type=int,
        default=128,
        help='Maximum sequence length (default: 128)'
    )
    argument_parser.add_argument(
        '--test_size',
        type=float,
        default=0.2,
        help='Fraction of training data used for evaluating the model (default: 0.2)'
    )
    argument_parser.add_argument(
        '--train_batch_size',
        type=int,
        default=16,
        help='Batch size for training (default: 16)'
    )
    argument_parser.add_argument(
        '--num_epochs',
        type=int,
        default=10,
        help='Number of epochs for training (default: 10)'
    )
    argument_parser.add_argument(
        '--train_output_path',
        type=str,
        default='assets/model.pth',
        help='Path to save the trained model (default: assets/model.pth)'
    )
    argument_parser.add_argument(
        '--training_data',
        type=str,
        default='assets/training_dataset.csv',
        help='Path to the training dataset CSV file (required for training mode)'
    )
    argument_parser.add_argument(
        '--output_path',
        default='assets/classified_posts.csv',
        help='Path to save classified posts'
    )
    if individual:
        argument_parser.add_argument(
            '--input_path',
            type=str,
            default='assets/parsed_posts.csv',
            help='Path to the parsed posts to classify'
        )


def add_analyzer_arguments(argument_parser, individual=True):
    if individual:
        argument_parser.add_argument(
            '--input_path',
            type=str,
            default='assets/classified_posts.csv',
            help='Path to classified posts to analyze'
        )


def add_silence_argument(argument_parser):
    argument_parser.add_argument(
        '--quiet',
        action='store_true',
        help='Quiet output (print less)'
    )


def create_parser(module_name):
    argument_parser = argparse.ArgumentParser()

    if module_name == "scraper":
        add_scraper_arguments(argument_parser)
    elif module_name == "parser":
        add_parser_arguments(argument_parser)
    elif module_name == "classifier":
        add_classifier_arguments(argument_parser)
    elif module_name == "analyzer":
        add_analyzer_arguments(argument_parser)
    elif module_name == "main":
        add_scraper_arguments(argument_parser, False)
        add_parser_arguments(argument_parser, False)
        add_classifier_arguments(argument_parser, False)
        add_analyzer_arguments(argument_parser, False)

    add_silence_argument(argument_parser)

    return argument_parser
