import configparser
import time
import asyncio
from hashlib import md5
from playwright.async_api import async_playwright
from ..printer import print_scraper_no_posts_found, print_scraper_metrics, print_scraper_new_scrape_heading


async def load_credentials():
    config = configparser.ConfigParser()
    config.read("assets/credentials.ini")

    return config["login"]["username"], config["login"]["password"], config["login"]["email"]


async def initialize_browser(headless=False):
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=headless)
    context = await browser.new_context()
    await context.route("**/*", block_non_essential_requests)

    return playwright, browser, context


async def block_non_essential_requests(route, request):
    if request.resource_type in ["image", "media", "stylesheet", "font", "other"]:
        await route.abort()
    else:
        await route.continue_()


async def login(page, username, password, email):
    await page.goto("https://x.com/login", wait_until="networkidle")
    await page.fill("input[name='text']", username)
    await page.click("button:has(div:has(span:has-text('Next')))")
    await page.wait_for_selector("input[name='password']")
    await page.fill("input[name='password']", password)
    await page.click("button:has(div:has(span:has(span:has-text('Log in'))))")

    if await page.is_visible("input[name='text']"):
        await page.fill("input[name='text']", email)
        await page.click("button:has(div:has(span:has(span:has-text('Next'))))")

    await page.wait_for_selector("div:has-text('What is happening?')", timeout=5000)


async def scrape_posts(page, url, num_posts=100):
    await page.goto(url)
    await page.wait_for_timeout(10000)

    post_hashes = set()
    complete_posts = []

    while len(complete_posts) < num_posts:
        posts = await page.query_selector_all("article")
        if not posts:
            print_scraper_no_posts_found()
            break

        for post in posts:
            text_content = await post.inner_text()
            post_hash = md5(text_content.encode('utf-8')).hexdigest()

            if post_hash not in post_hashes:
                post_hashes.add(post_hash)
                complete_posts.append(text_content)

            if len(complete_posts) >= num_posts:
                break

        await page.evaluate("window.scrollBy(0, window.innerHeight);")
        await asyncio.sleep(0.5)

    return complete_posts[:num_posts]


async def login_and_scrape_x_posts(account_id, url, num_posts=100, headless=False):
    print_scraper_new_scrape_heading(account_id, num_posts)
    username, password, email = await load_credentials()

    try:
        playwright, browser, context = await initialize_browser(headless=headless)
        page = await context.new_page()

        await login(page, username, password, email)
        posts = await scrape_posts(page, url, num_posts)

        await browser.close()
        await playwright.stop()

        return posts

    except Exception as e:
        print(f"Error in login_and_scrape_x_posts for {account_id}: {e}")

        return []


async def scrape_x_accounts(accounts, num_posts=100, headless=False):
    start_time = time.time()

    try:
        tasks = [
            login_and_scrape_x_posts(account_id, url, num_posts=num_posts, headless=headless)
            for account_id, url in accounts.items()
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    except Exception as e:
        print(f"Error in scrape_x_accounts: {e}")
        results = []

    end_time = time.time()

    scraped_posts = dict(zip(accounts.keys(), results))

    print_scraper_metrics(end_time, start_time, scraped_posts, num_posts * len(accounts))

    return scraped_posts
