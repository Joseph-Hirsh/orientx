import pandas as pd
import time
from .dates_parser import parse_date
from .metrics_parser import parse_metric
from ..printer.parser_printer import print_parser_heading, print_parser_error, print_parser_completed


def parse_x_posts(scraped_data):
    start_time = time.time()
    parsed_tweets = []
    total_posts, successfully_parsed = 0, 0

    for account_id, posts in scraped_data.items():
        print_parser_heading(posts, account_id)
        account_results, parsed, total = parse_account_posts(account_id, posts)
        parsed_tweets.extend(account_results)
        successfully_parsed += parsed
        total_posts += total

    end_time = time.time()
    parsed_tweets_df = pd.DataFrame(parsed_tweets)

    print_parser_completed(end_time, start_time, successfully_parsed, total_posts, parsed_tweets_df)

    return parsed_tweets_df


def parse_account_posts(account_id, posts):
    parsed_tweets = []
    successfully_parsed, total_posts = 0, 0

    for tweet_data in posts:
        total_posts += 1
        try:
            tweet_dict = parse_single_post(account_id, tweet_data)
            parsed_tweets.append(tweet_dict)
            successfully_parsed += 1
        except Exception as e:
            print_parser_error(tweet_data.split('\n'), e)

    return parsed_tweets, successfully_parsed, total_posts


def parse_single_post(account_id, tweet_data):
    tweet_data = clean_media_placeholder(tweet_data)
    lines = tweet_data.strip().split('\n')

    reposted, reposter_name, pinned = check_post_status(lines)
    poster_name, poster_handle, timestamp, content_lines = extract_post_info(lines, reposted, pinned)

    timestamp = parse_date(timestamp)
    content = format_content(content_lines)
    replies, retweets, likes, views = parse_engagement_metrics(lines)

    return {
        'account_id': account_id,
        'poster_name': poster_name,
        'poster_handle': poster_handle,
        'reposted': reposted,
        'reposter_name': reposter_name,
        'pinned': pinned,
        'timestamp': timestamp,
        'content': content,
        'replies': replies,
        'retweets': retweets,
        'likes': likes,
        'views': views,
    }


def clean_media_placeholder(tweet_data):
    return tweet_data.replace("The media could not be played.\nReload", "")


def check_post_status(lines):
    reposted, reposter_name = False, None
    pinned = False

    if 'reposted' in lines[0]:
        reposted = True
        reposter_name = lines[0].replace(' reposted', '').strip()
    elif 'Pinned' in lines[0]:
        pinned = True

    return reposted, reposter_name, pinned


def extract_post_info(lines, reposted, pinned):
    if reposted:
        poster_name = lines[1].strip()
        poster_handle = lines[2].strip()
        timestamp = lines[4].strip()
        content_lines = lines[5:-4]
    elif pinned:
        poster_name = lines[1].strip()
        poster_handle = lines[2].strip()
        timestamp = lines[4].strip()
        content_lines = lines[5:-4]
    else:
        poster_name = lines[0].strip()
        poster_handle = lines[1].strip()
        timestamp = lines[3].strip()
        content_lines = lines[4:-4]

    return poster_name, poster_handle, timestamp, content_lines


def format_content(content_lines):
    return ' '.join(line.strip() for line in content_lines if line.strip())


def parse_engagement_metrics(lines):
    replies = parse_metric(lines[-4].strip()) if len(lines) >= 4 else 0
    retweets = parse_metric(lines[-3].strip()) if len(lines) >= 4 else 0
    likes = parse_metric(lines[-2].strip()) if len(lines) >= 4 else 0
    views = parse_metric(lines[-1].strip()) if len(lines) >= 4 else 0

    return replies, retweets, likes, views
