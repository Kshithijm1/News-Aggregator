## News Aggregator System

This project is an asynchronous news aggregator that fetches and stores news articles from various sources. It is implemented using Python, with libraries including aiohttp for asynchronous HTTP requests, BeautifulSoup for parsing HTML, and SQLAlchemy for database operations.

### Prerequisites

- Python 3.6+
- aiohttp
- asyncio
- BeautifulSoup4
- SQLAlchemy
- APScheduler
- PostgreSQL

You can install the necessary libraries using pip:
```bash
pip install aiohttp beautifulsoup4 sqlalchemy apscheduler
```

### Configuration

The configuration for news sources is stored in a `config.json` file, which should include the URL, CSS selectors for scraping, and names for each news source.

### Database Setup

A PostgreSQL database is used to store the fetched news articles. The schema includes a `news` table with columns for the `title` (primary key) and `url`.

### Features

- **Asynchronous Fetching**: Utilizes `aiohttp` to fetch news content asynchronously.
- **HTML Parsing**: Parses the HTML content to extract news headlines using BeautifulSoup and a CSS selector provided in the configuration.
- **Database Storage**: Stores news articles in a PostgreSQL database using SQLAlchemy.
- **Scheduled Fetching**: Uses APScheduler to schedule news fetching at regular intervals (every 30 minutes).

### Functions

1. **`fetch_html(session, url)`**: Asynchronously fetches HTML content from the specified URL.
2. **`parse_news(html, css_selector)`**: Parses the HTML content to extract news headlines.
3. **`fetch_news(name, url, selector)`**: Fetches news from a single source and parses the headlines.
4. **`aggregate_news()`**: Aggregates news from all configured sources.
5. **`save_news_to_db(news_items)`**: Saves the fetched news articles to the database.
6. **`schedule_news_fetch()`**: Schedules the fetching of news at regular intervals.

### Running the Project

To run the project, ensure you have the required dependencies installed and a PostgreSQL database set up as described. Execute the `main` function to start the asynchronous news fetching process.

### Example Usage

```python
if __name__ == "__main__":
    main()
```

This script will continuously fetch and update the news database every 30 minutes, running indefinitely unless stopped manually.

### Maintenance and Logging

Logging is configured to provide detailed error messages and information about the fetching and saving processes, aiding in troubleshooting and monitoring the system's performance.

---
