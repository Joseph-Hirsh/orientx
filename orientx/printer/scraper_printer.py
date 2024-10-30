from orientx import config
from .pretty_printer import pretty_print


def print_scraper_new_scrape_heading(account_id, max_posts, username):
    if not config.QUIET:
        pretty_print(f"[i] Scraping {max_posts} posts from {account_id} using scraper account {username}")


def print_scraper_passing_extra_security():
    if not config.QUIET:
        pretty_print(f"(x.com is suspicious: passing extra security check)")


def print_scraper_error(account_id, e):
    if not config.QUIET:
        pretty_print(f"[!] Error scraping {account_id}: {e}")


def print_scraper_no_posts_found(account_id):
    if not config.QUIET:
        pretty_print(f"[!] No posts found for {account_id}!")


def print_scraper_metrics(end_time, start_time, scraped_posts, num_posts):
    if not config.QUIET:
        elapsed_time = end_time - start_time
        posts_scraped = sum(len(internal) for internal in scraped_posts.values())
        posts_per_minute = (posts_scraped * 60 / elapsed_time) if elapsed_time > 0 else 0
        success_rate = (posts_scraped / num_posts) * 100 if posts_scraped > 0 else 0

        print_type = "[!]" if posts_scraped == 0 else "[-]" if posts_scraped < num_posts / 2 else "[+]"

        pretty_print(
            f"{print_type} Scraped {posts_scraped}/{num_posts} posts in {elapsed_time:.3f} seconds "
            f"({posts_per_minute:.3f} posts per minute with {success_rate:.3f}% success rate)"
        )

        for key, value in scraped_posts.items():
            pretty_print(f"    {key}: {len(value)}")
