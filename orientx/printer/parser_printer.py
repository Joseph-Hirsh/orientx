from orientx import config
from .pretty_printer import pretty_print


def print_parser_heading(posts, account_id):
    if not config.QUIET:
        pretty_print(f"[i] Parsing {len(posts)} posts from {account_id}")


def print_parser_error(lines, error_message):
    if not config.QUIET:
        pretty_print(f"[-] Error parsing post: {lines}")
        pretty_print(f"    Reason: {error_message}\n")


def print_parser_completed(end_time, start_time, successfully_parsed, total_posts, parsed_tweets):
    if not config.QUIET:
        elapsed_time = end_time - start_time
        posts_per_second = successfully_parsed / elapsed_time if elapsed_time > 0 else 0
        success_rate = (successfully_parsed / total_posts) * 100 if total_posts > 0 else 0

        pretty_print(
            f"[+] Parsed {successfully_parsed}/{total_posts} posts in {elapsed_time:.3f} seconds "
            f"({posts_per_second:.3f} posts per second with {success_rate:.3f}% success rate)"
        )

        if not parsed_tweets.empty:
            account_counts = parsed_tweets['account_id'].value_counts()
            for account_id, count in account_counts.items():
                pretty_print(f"    {account_id}: {count}")
