import os
import json
import requests
import django
django.setup()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_scraper.settings')

from xmltodict import parse
from datetime import datetime
from typing import Union, Text, List
from news_scraper.api.models import News

from celery import shared_task
from news_scraper.logger import LOGGER
from news_scraper.settings import SCRAPING_URL, SYMBOL_TYPES, DEFAULT_QUERY_PARAMS


def handle_url(url, query_params):
    return url + "?" + "&".join(f"{key}={value}" for key, value in query_params.items()) if query_params else url


def _parse_item(item, symbol_type) -> Union[News, None]:
    try:
        item_date = item.get("pubDate")
        date = " ".join(t for t in item_date.split(",")[-1].strip().split(" "))
        converted_date = datetime.strptime(date, '%d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d %H:%M:%S')

        model_item = News(
            guid=item.get("guid", {}).get("#text"),
            symbol_type=symbol_type,
            title=item.get("title"),
            description=item.get("description"),
            publish_date=converted_date,
            link=item.get("link")
        )

    except Exception as _exc:
        LOGGER.debug(f"Problem with parsing item: {item}")
        LOGGER.debug(f"Reason: {_exc}")
        return None

    return model_item


def parse_response(res: Text, symbol: Text) -> Union[List[News], None]:
    try:
        parser = parse(res)
        parsed_res = json.loads(json.dumps(parser))
        items = parsed_res.get('rss', {}).get('channel', {}).get('item')

        return [
            _parse_item(item, symbol) for item in items
        ]

    except Exception as _exc:
        LOGGER.debug(f"Problem with response parser.")
        LOGGER.debug(f"Reason: {_exc}")
        return None


def flush_data(item):
    if not News.objects.filter(guid=item.guid).exists():
        item.save()


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
