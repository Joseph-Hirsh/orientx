import configparser
import time
import asyncio
from hashlib import md5
from playwright.async_api import async_playwright
from ..printer import print_scraper_no_posts_found, print_scraper_metrics, print_scraper_new_scrape_heading, \
    print_scraper_error, print_scraper_passing_extra_security


async def login(page, username, password, email):
    await page.goto("https://x.com/login", wait_until="networkidle")
    await page.fill("input[name='text']", username)
    await page.click("button:has(div:has(span:has-text('Next')))")

    try:
        await page.wait_for_selector("span:has-text('Phone or email')", timeout=2000)
    except:
        pass

    if await page.is_visible("span:has-text('Phone or email')"):
        print_scraper_passing_extra_security()

        await page.fill("input[name='text']", email)
        await page.click("button:has(div:has(span:has(span:has-text('Next'))))")

    await page.wait_for_selector("input[name='password']")
    await page.fill("input[name='password']", password)
    await page.click("button:has(div:has(span:has(span:has-text('Log in'))))")

    await page.wait_for_selector("div:has-text('What is happening?')", timeout=5000)


async def load_credentials(account_index):
    config = configparser.ConfigParser()
    config.read("assets/credentials.ini")
    account_section = config.sections()[account_index % len(config.sections())]
    credentials = config[account_section]

    return credentials["username"], credentials["password"], credentials["email"]


async def initialize_browser(headless=False):
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=headless)
    context = await browser.new_context()
    await context.route("**/*", block_non_essential_requests)

    return playwright, browser, context


async def block_non_essential_requests(route, request):
    if request.resource_type in {"image", "media", "stylesheet", "font", "other"}:
        await route.abort()
    else:
        await route.continue_()


async def scrape_posts(page, url, num_posts=100, mode="auto", check_interval=0.001):
    await page.goto(url)
    await page.wait_for_timeout(10000)

    post_hashes, complete_posts = set(), []

    async def collect_new_posts():
        posts = await page.query_selector_all("article")
        for post in posts:
            text_content = await post.inner_text()

            split_static_text_content = text_content.split("\n")[:5]
            static_text_content = "\n".join(split_static_text_content)

            post_hash = md5(static_text_content.encode('utf-8')).hexdigest()

            if post_hash not in post_hashes:
                post_hashes.add(post_hash)
                complete_posts.append(text_content)

            if len(complete_posts) >= num_posts:
                return True
        return False

    if mode == "auto":
        while len(complete_posts) < num_posts:
            if await collect_new_posts():
                break
            await page.evaluate("window.scrollBy(0, window.innerHeight);")
            await asyncio.sleep(0.5)
    else:
        while len(complete_posts) < num_posts:
            await collect_new_posts()
            await asyncio.sleep(check_interval)

    return complete_posts[:num_posts]


async def login_and_scrape_x_posts(account_id, url, num_posts=100, headless=False, account_index=0, mode="auto"):
    username, password, email = await load_credentials(account_index)
    print_scraper_new_scrape_heading(account_id, num_posts, username)

    try:
        playwright, browser, context = await initialize_browser(headless=headless)
        page = await context.new_page()

        await login(page, username, password, email)
        posts = await scrape_posts(page, url, num_posts=num_posts, mode=mode)

        if not posts:
            print_scraper_no_posts_found(account_id)

        await browser.close()
        await playwright.stop()

        return posts
    except Exception as e:
        print_scraper_error(account_id, e)

        return []


async def scrape_x_accounts(accounts, num_posts=100, batch_size=2, headless=False, scroll_mode="auto"):
    start_time = time.time()
    account_items = list(accounts.items())
    scraped_posts = {}

    tasks = [
        login_and_scrape_x_posts(account_id, url, num_posts=num_posts, headless=headless, account_index=i,
                                 mode=scroll_mode)
        for i, (account_id, url) in enumerate(account_items)
    ]

    if scroll_mode == "manual":
        for i, task in enumerate(tasks):
            result = await task
            account_id, _ = account_items[i]
            scraped_posts[account_id] = result
    else:
        for i in range(0, len(tasks), batch_size):
            results = await asyncio.gather(*tasks[i:i + batch_size], return_exceptions=True)
            scraped_posts.update(
                {account_id: result for (account_id, _), result in zip(account_items[i:i + batch_size], results)}
            )

    print_scraper_metrics(time.time(), start_time, scraped_posts, num_posts * len(accounts))

    return scraped_posts

