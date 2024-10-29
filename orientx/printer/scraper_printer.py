from orientx import config
from .pretty_printer import pretty_print


def print_scraper_new_scrape_heading(url, max_posts):
    if config.VERBOSE:
        pretty_print(f"[i] Scraping {max_posts} posts from {url}")


def print_scraper_no_posts_found():
    if config.VERBOSE:
        pretty_print("[!] No posts found!")


def print_scraper_metrics(end_time, start_time, scraped_posts, num_posts):
    if config.VERBOSE:
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
