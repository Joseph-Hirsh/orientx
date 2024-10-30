import pandas as pd

from orientx import config
from orientx.arguments import create_parser, validate_arguments
from orientx.classifier import ClassificationPipeline, load_data, classify_x_posts
from orientx.printer import print_parameters, print_driver_df


def inference(args):
    pipeline = ClassificationPipeline(model_name='bert-base-uncased', num_classes=args.num_classes)
    pipeline.load_model(args.model_path)

    parsed_posts_df = pd.read_csv(args.input_path)

    classifications_df = classify_x_posts(pipeline, parsed_posts_df)
    classifications_df.to_csv(args.output_path, index=False)
    print_driver_df("Classified Posts", classifications_df)


def train(args):
    (train_texts, train_labels), (val_texts, val_labels) = load_data(args.training_data, test_size=args.test_size)

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
    parser = create_parser('classifier')
    args = parser.parse_args()
    validate_arguments(args, 'classifier')

    config.QUIET = args.quiet
    print_parameters(args)

    if args.mode == "train":
        train(args)
    elif args.mode == "inference":
        inference(args)


if __name__ == "__main__":
    main()
