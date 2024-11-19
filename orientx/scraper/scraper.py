import configparser
import json
import time
import asyncio
from hashlib import md5
import random
from playwright.async_api import async_playwright
import os
from stem import Signal
from stem.control import Controller
from ..printer import (
    print_scraper_no_posts_found,
    print_scraper_metrics,
    print_scraper_new_scrape_heading,
    print_scraper_error,
    print_scraper_passing_extra_security,
)


# Helper Functions for Proxy and Browser Setup
async def request_new_ip():
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate("one")
            controller.signal(Signal.NEWNYM)
            print("Requested new IP address from Tor")
    except Exception as e:
        print(f"Error requesting new IP: {e}")


async def initialize_browser(headless=False, proxy_server='socks5://localhost:9050'):
    await request_new_ip()

    playwright = await async_playwright().start()

    launch_options = {
        "headless": headless,
        "proxy": {"server": proxy_server} if proxy_server else None,
        "args": []
    }

    browser = await playwright.chromium.launch(**launch_options)
    context = await browser.new_context()
    await context.route("**/*", block_unnecessary_requests)

    page = await context.new_page()
    page.on('console', lambda msg: print(f"Console log: {msg.text}"))

    await verify_proxy(context)

    return playwright, context, page


async def block_unnecessary_requests(route, request):
    if request.resource_type in {"image", "media", "stylesheet", "font", "other"}:
        await route.abort()
    else:
        await route.continue_()


async def verify_proxy(context):
    page = await context.new_page()
    response = await page.goto('https://httpbin.org/ip')
    ip_data = await response.json()
    print(f"Current IP address via proxy: {ip_data['origin']}")
    await page.close()


# Account Scraping and Login Functions
async def scrape_account(account_id, account_url, num_posts=100, headless=False, account_index=0,
                         session_file="user_session.json"):
    username, password, email = load_account_credentials(account_index)
    print_scraper_new_scrape_heading(account_id, num_posts, username)

    collected_posts = []
    try:
        playwright, context, page = await initialize_browser(headless=headless)

        await load_or_update_session(context, page, username, password, email, session_file)
        collected_posts = await scrape_account_posts(page, account_url, target_post_count=num_posts)
        if not collected_posts:
            print_scraper_no_posts_found(account_id)

        await context.close()
        await playwright.stop()
    except Exception as e:
        print_scraper_error(account_id, e)

    return collected_posts


def check_cookie_expiration(cookies):
    current_time = time.time()

    for cookie in cookies:
        if cookie['expires'] == -1 or cookie['expires'] is None:
            continue

        if cookie['expires'] < current_time:
            return True

    return False


async def load_or_update_session(context, page, username, password, email, session_file):
    if os.path.exists(session_file) and os.path.getsize(session_file) > 0:
        with open(session_file, "r") as f:
            session_data = json.load(f)
            if isinstance(session_data, list):
                if check_cookie_expiration(session_data):
                    await reenter_credentials_and_save_session(page, username, password, email, session_file, context)
                else:
                    await context.add_cookies(session_data)
            else:
                print("Invalid session data format.")
    else:
        print("Session file is either missing or empty.")
        await reenter_credentials_and_save_session(page, username, password, email, session_file, context)


async def reenter_credentials_and_save_session(page, username, password, email, session_file, context):
    await enter_credentials(page, username, password, email)
    session_data = await context.cookies()
    with open(session_file, "w") as f:
        json.dump(session_data, f)


async def enter_credentials(page, username, password, email):
    await page.goto("https://x.com/login", wait_until="networkidle")
    await page.fill("input[name='text']", username)
    await page.click("button:has(div:has(span:has-text('Next')))")

    await handle_security_prompt(page, email)

    await page.fill("input[name='password']", password)
    await page.click("button:has(div:has(span:has(span:has-text('Log in'))))")

    await page.wait_for_selector("div:has-text('What is happening?')", timeout=50000)


async def handle_security_prompt(page, email):
    try:
        await page.wait_for_selector("span:has-text('Phone or email')", timeout=5000)
    except:
        return
    print_scraper_passing_extra_security()
    await page.fill("input[name='text']", email)
    await page.click("button:has(div:has(span:has(span:has_text('Next'))))")


# Scraping Functions
async def scrape_account_posts(page, account_url, target_post_count=100, scroll_delay_range=(1.5, 3),
                               long_pause_frequency=8):
    await page.goto(account_url)
    await page.wait_for_timeout(5000)

    unique_posts = set()
    collected_posts = []

    async def extract_posts():
        nonlocal collected_posts
        posts = await page.query_selector_all("article")

        for post in posts:
            content = await post.inner_text()
            static_preview = "\n".join(content.split("\n")[:5])
            post_hash = md5(static_preview.encode("utf-8")).hexdigest()

            if post_hash not in unique_posts:
                unique_posts.add(post_hash)
                collected_posts.append(content)

            if len(collected_posts) >= target_post_count:
                return True
        return False

    scroll_count = 0

    while len(collected_posts) < target_post_count:
        if await extract_posts():
            break
        await scroll_page(page, delay_range=scroll_delay_range)
        scroll_count += 1

        if scroll_count % long_pause_frequency == 0:
            long_pause = random.uniform(15, 30)
            print(f"Taking a long pause for {long_pause:.2f} seconds...")
            await asyncio.sleep(long_pause)

    return collected_posts[:target_post_count]


async def scroll_page(page, delay_range=(2, 5)):
    offset = random.uniform(200, 400)
    await page.evaluate(f"window.scrollBy(0, {offset});")
    delay = random.uniform(*delay_range)
    print(f"Scrolling by {offset:.2f}px and waiting for {delay:.2f} seconds...")
    await asyncio.sleep(delay)


# Utility Functions
def load_account_credentials(account_index, credentials_file="assets/credentials.ini"):
    config = configparser.ConfigParser()
    config.read(credentials_file)
    account_sections = config.sections()
    selected_account = account_sections[account_index % len(account_sections)]
    credentials = config[selected_account]

    return credentials["username"], credentials["password"], credentials["email"]


# Scraping Multiple Accounts
async def scrape_x_accounts(account_data, num_posts=100, batch_size=1, headless=False):
    start_time = time.time()
    tasks = [
        scrape_account(account_id, account_url, num_posts, headless, i)
        for i, (account_id, account_url) in enumerate(account_data.items())
    ]

    scraped_data = {}
    for batch_start in range(0, len(tasks), batch_size):
        batch_tasks = tasks[batch_start:batch_start + batch_size]
        results = await asyncio.gather(*batch_tasks, return_exceptions=True)

        for (account_id, _), result in zip(list(account_data.items())[batch_start:batch_start + batch_size], results):
            scraped_data[account_id] = result

    print_scraper_metrics(time.time(), start_time, scraped_data, num_posts * len(account_data))
    return scraped_data
