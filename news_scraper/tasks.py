import os
import requests
import django
django.setup()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_scraper.settings')

from celery import shared_task
from news_scraper.logger import LOGGER
from news_scraper.settings import SCRAPING_URL, SYMBOL_TYPES, DEFAULT_QUERY_PARAMS
from news_scraper.tasks_utils import handle_url, parse_response, flush_data


@shared_task
def collect_data():
    headers = {
        'User-Agent': 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
    }

    for symbol in SYMBOL_TYPES:

        DEFAULT_QUERY_PARAMS.update(
            {"s": symbol}
        )

        parsed_url = handle_url(SCRAPING_URL, DEFAULT_QUERY_PARAMS)
        LOGGER.debug(f"SCRAPING_URL={parsed_url}...")

        res = requests.get(parsed_url, headers=headers)

        if res.status_code != 200:
            LOGGER.warning(f"There is problem with fetching data from {SCRAPING_URL}.")
            LOGGER.warning(f"Status code: {res.status_code}. Response: {res}")
            return

        parsed_response = parse_response(res.text, symbol)

        if parsed_response:
            [
                flush_data(item) for item in parsed_response
            ]

        else:
            LOGGER.debug(f"No data for symbol: {symbol}...")
