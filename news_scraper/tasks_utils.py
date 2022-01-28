import json
from xmltodict import parse
from datetime import datetime
from typing import Union, Text, List

from news_scraper.api.models import News
from news_scraper.logger import LOGGER


def handle_url(url, query_params=None):
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


def flush_data(item) -> None:
    if not News.objects.filter(guid=item.guid).exists():
        item.save()
