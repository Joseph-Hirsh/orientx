from orientx import config
from .pretty_printer import pretty_print


def print_classifier_loading_failed(row):
    if config.VERBOSE:
        pretty_print(f"[-] Skipping malformed row: {row}")


def print_classifier_training_heading(epochs):
    if config.VERBOSE:
        pretty_print(f"[i] Training model for {epochs} epochs")


def print_classifier_epoch_update(epoch, epochs):
    if config.VERBOSE:
        percent_complete = epoch * 100 / epochs
        pretty_print(f"[i] Running epoch {epoch + 1} of {epochs} ({percent_complete:.2f}% complete)")


def print_classifier_loss_metric(epoch, loss):
    if config.VERBOSE:
        pretty_print(f"[+] Loss after epoch {epoch + 1}: {loss.item():.4f}")


def print_classifier_training_complete(accuracy, report, train_output_path):
    if config.VERBOSE:
        pretty_print("[+] Training complete:")
        pretty_print(report)
        pretty_print(f"Validation accuracy = {accuracy}; model saved to {train_output_path}")


def print_classifier_classify_heading(posts_df):
    if config.VERBOSE:
        pretty_print(f"[i] Classifying {len(posts_df)} posts")


def print_classifier_classify_complete(end_time, start_time, classifications):
    if config.VERBOSE:
        num_classifications = len(classifications)
        elapsed_time = end_time - start_time
        posts_per_minute = num_classifications * 60 / elapsed_time if elapsed_time > 0 else 0

        pretty_print(
            f"[+] Classified {num_classifications} posts in {elapsed_time:.3f} seconds "
            f"({posts_per_minute:.3f} posts per minute)"
        )
