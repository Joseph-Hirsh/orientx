import argparse
import os


def validate_arguments(args):
    pass
    # current_dir = os.getcwd()
    #
    # if hasattr(args, 'num_posts') and not (isinstance(args.num_posts, int) and args.num_posts >= 1):
    #     raise ValueError("num_posts must be an integer greater than or equal to 1.")
    # if hasattr(args, 'num_classes') and not (isinstance(args.num_classes, int) and args.num_classes >= 1):
    #     raise ValueError("num_classes must be an integer greater than or equal to 1.")
    # if hasattr(args, 'mode') and args.mode == 'run':
    #     model_path = args.model_path
    #     full_model_path = os.path.join(current_dir, model_path)
    #     if not os.path.isfile(full_model_path):
    #         raise ValueError(f"model_path '{full_model_path}' must be a valid file path.")
    # if hasattr(args, 'num_epochs') and not (isinstance(args.num_epochs, int) and args.num_epochs >= 1):
    #     raise ValueError("num_epochs must be an integer greater than or equal to 1.")
    # if hasattr(args, 'max_input_length') and not (isinstance(args.max_input_length, int) and args.max_input_length >= 1):
    #     raise ValueError("max_input_length must be an integer greater than or equal to 1.")
    # if hasattr(args, 'train_batch_size') and not (
    #         isinstance(args.train_batch_size, int) and args.train_batch_size >= 1):
    #     raise ValueError("train_batch_size must be an integer greater than or equal to 1.")
    # if hasattr(args, 'scrape_batch_size') and not (
    #         isinstance(args.scrape_batch_size, int) and args.scrape_batch_size >= 1):
    #     raise ValueError("scrape_batch_size must be an integer greater than or equal to 1.")
    # if hasattr(args, 'learning_rate') and not (isinstance(args.learning_rate, float) and args.learning_rate >= 0):
    #     raise ValueError("learning_rate must be a non-negative float.")


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
    elif module_name == 'analyzer':
        add_analyzer_arguments(argument_parser)
    elif module_name == "main":
        add_scraper_arguments(argument_parser, individual=False)
        add_parser_arguments(argument_parser, individual=False)
        add_classifier_arguments(argument_parser, individual=False)

    add_silence_argument(argument_parser)

    return argument_parser
