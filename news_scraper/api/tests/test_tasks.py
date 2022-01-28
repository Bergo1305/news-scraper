from django.test import TestCase
from news_scraper.tasks_utils import parse_response, _parse_item, handle_url


class TestTasks(TestCase):

    SCRAPING_URL = "https://test.yahoo.com/rss/2.0/headline"

    TASK_TEST_1 = {
       "description": "Meta Platforms (NASDAQ: FB), the tech giant formerly known as Facebook, is often considered a top play on the growing metaverse, which could eventually blur the lines between our physical and digital worlds with virtual reality and augmented reality platforms.  Meta enjoys a first-mover's advantage in this space through Oculus, the virtual reality company it acquired in 2014.  Oculus' latest VR device, the Quest 2, reportedly topped ten million shipments last year to become the world's most popular stand-alone VR headset by a wide margin.",
       "guid": {
          "@isPermaLink": "false",
          "#text": "7cdfc06d-cd78-3faa-8fe6-f0ab035fd932"
       },
       "link": "https://finance.yahoo.com/m/7cdfc06d-cd78-3faa-8fe6-f0ab035fd932/1-green-flag-and-1",
       "pubDate": "Sun, 23 Jan 2022 11:47:00 +0000",
       "title": "1 Green Flag and 1 Red Flag for Meta's Metaverse Dreams"
    }

    TASK_TEST_2 = {
        "description": "Meta Platforms (NASDAQ: FB), the tech giant formerly known as Facebook, is often considered a top play on the growing metaverse, which could eventually blur the lines between our physical and digital worlds with virtual reality and augmented reality platforms.  Meta enjoys a first-mover's advantage in this space through Oculus, the virtual reality company it acquired in 2014.  Oculus' latest VR device, the Quest 2, reportedly topped ten million shipments last year to become the world's most popular stand-alone VR headset by a wide margin.",
        "guid": {
            "@isPermaLink": "false",
        },
        "link": "https://finance.yahoo.com/m/7cdfc06d-cd78-3faa-8fe6-f0ab035fd932/1-green-flag-and-1",
        "pubDate": "Sun, 11:47:00 +0000",
        "title": "1 Green Flag and 1 Red Flag for Meta's Metaverse Dreams"
    }

    def test_url_resolver_no_query(self):
        url = handle_url(TestTasks.SCRAPING_URL)

        self.assertEqual(url, TestTasks.SCRAPING_URL)

    def test_url_resolver_with_query(self):
        query_params = {'test1': 1, 'test2': 2}
        url = handle_url(TestTasks.SCRAPING_URL, query_params)

        self.assertEqual(url, TestTasks.SCRAPING_URL + "?test1=1&test2=2")

    def test_parse_item(self):
        item = _parse_item(TestTasks.TASK_TEST_1, "symbol")

        self.assertEqual(item.guid, TestTasks.TASK_TEST_1['guid']['#text'])
        self.assertEqual(item.link, TestTasks.TASK_TEST_1['link'])
        self.assertEqual(item.publish_date, "2022-01-23 11:47:00")
        self.assertEqual(item.description, TestTasks.TASK_TEST_1['description'])
        self.assertEqual(item.symbol_type, "symbol")

    def test_parse_bad_item(self):
        item = _parse_item(TestTasks.TASK_TEST_2, "symbol")

        self.assertEqual(item, None)


