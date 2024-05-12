import aiohttp
import asyncio
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
from sqlalchemy import create_engine, Table, Column, String, MetaData
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
with open('config.json', 'r') as file:
    config = json.load(file)
    news_sources = config['news_sources']

# Database setup
engine = create_engine('postgresql://username:password@localhost/newsdb')
metadata = MetaData()
news_table = Table('news', metadata,
                   Column('title', String, primary_key=True),
                   Column('url', String))
metadata.create_all(engine)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

async def fetch_html(session, url):
    """ Asynchronously fetch HTML content from the specified URL """
    try:
        async with session.get(url, headers=headers, timeout=10) as response:
            response.raise_for_status()
            return await response.text()
    except Exception as e:
        logging.error(f'Error fetching {url}: {str(e)}')
        return None

def parse_news(html, css_selector):
    """ Parse news headlines and URLs using a CSS selector """
    soup = BeautifulSoup(html, 'html.parser')
    headlines = []
    for link in soup.select(css_selector):
        href = link['href']
        if not href.startswith('http'):
            href = urljoin(url, href)
        headlines.append((link.text.strip(), href))
    return headlines

async def fetch_news(name, url, selector):
    """ Fetch and parse news from a single source """
    async with aiohttp.ClientSession() as session:
        html = await fetch_html(session, url)
        if html:
            return parse_news(html, selector)
    return []

async def aggregate_news():
    """ Aggregate news from various sources using asynchronous calls """
    tasks = []
    for source in news_sources:
        tasks.append(fetch_news(source['name'], source['url'], source['selector']))
    results = await asyncio.gather(*tasks)
    return [headline for source in results for headline in source]

def save_news_to_db(news_items):
    """ Save news items to the database """
    with engine.connect() as conn:
        for title, url in news_items:
            conn.execute(news_table.insert().values(title=title, url=url))
    logging.info('News has been saved to the database')

async def schedule_news_fetch():
    """ Schedule news fetching every 30 minutes """
    scheduler = AsyncIOScheduler()
    scheduler.add_job(aggregate_news, 'interval', minutes=30)
    scheduler.start()
    await asyncio.Event().wait()  # Run indefinitely

def main():
    asyncio.run(schedule_news_fetch())

if __name__ == "__main__":
    main()
