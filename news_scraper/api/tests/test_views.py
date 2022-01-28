from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpResponseBadRequest
from django.conf import settings
from news_scraper.api.views import handle_pagination_response


class TestViewsQueryParams(TestCase):

    client = Client()

    def test_news_no_query(self):

        response = self.client.get(reverse('news'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.__class__.__name__, HttpResponseBadRequest.__name__)

    def test_news_bad_query(self):

        query_param = {'bad_symbol': 'AAPL'}
        response = self.client.get(reverse('news'), query_param)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.__class__.__name__, HttpResponseBadRequest.__name__)

    def test_news_good_query(self):

        query_param = {'s': 'AAPL'}
        response = self.client.get(reverse('news'), query_param)
        self.assertEqual(response.status_code, 200)

    def test_news_no_query_in_list(self):
        query_param = {'s': 'symbol-test'}
        response = self.client.get(reverse('news'), query_param)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.__class__.__name__, HttpResponseBadRequest.__name__)


class TestPaginationHandler(TestCase):

    PAGINATION_TEST_1 = {
        "next": "http://localhost/api/news?page=2",
        "previous": None,
        "count": 100,
        "results": [
            {
                "guid": "545803d3-460d-3b7a-8e7e-bcf525737e0b",
                "symbol_type": "AAPL",
                "title": "Apple Reports Earnings Thursday. Why at Least One Analyst Is Cautious.",
                "description": "Apple bulls think strong iPhone sales could boost the top line, but Goldman Sachs analyst Rod Hall thinks the December-quarter report could disappoint.",
                "publish_date": "2022-01-26T13:37:00Z",
                "link": "https://finance.yahoo.com/m/545803d3-460d-3b7a-8e7e-bcf525737e0b/apple-reports-earnings.html?.tsrc=rss"
            }
        ]
    }

    PAGINATION_TEST_2 = {
        "next": None,
        "previous": None,
        "count": 0,
        "results": []
    }

    PAGINATION_TEST_3 = {
        "count": 52,
        "next": "http://localhost/api/news?page=3",
        "previous": "http://localhost/api/news?page=1",
        "results": [
            {
                "guid": "8ec56dce-550a-3be9-8001-ac660753b931",
                "symbol_type": "AAPL",
                "title": "Apple teases metaverse AR plans, stock jumps",
                "description": "Apple Inc teased its metaverse ambitions on Thursday as CEO Tim Cook talked expansion of the company's augmented reality apps, prompting strong investor response.  The company has 14,000 AR apps on its App Store, and Cook suggested this number will rise with further investment.  \"We see a lot of potential in this space and are investing accordingly,\" said Cook, in response to a question about its plans for the metaverse https://www.reuters.com/technology/what-is-metaverse-2021-10-18, a broad term that generally refers to shared virtual world environments that people can access via the internet.",
                "publish_date": "2022-01-28T01:00:19Z",
                "link": "https://finance.yahoo.com/news/apple-teases-metaverse-ar-plans-010019140.html?.tsrc=rss"
            },
            {
                "guid": "752235eb-7744-3e0f-8394-a34f0ebb3a1a",
                "symbol_type": "AAPL",
                "title": "Viral TikTok shows the ‘secret button’ hidden in the back of iPhone that can be used for anything",
                "description": "There is a hidden button located in the back of the iPhone, a viral TikTok has shown.  While the option to use the button has been in the Apple handset for years, a new video has brought awareness of it to a whole new set of people.  More than a million users have viewed just one video celebrating the new feature, which warns that people are using their iPhone wrong if they are not taking advantage of it.",
                "publish_date": "2022-01-28T00:16:19Z",
                "link": "https://www.independent.co.uk/tech/iphone-button-back-tap-tiktok-video-b2002283.html?.tsrc=rss"
            },
            {
                "guid": "a924f079-54bb-3617-a452-5a74a723eca3",
                "symbol_type": "AAPL",
                "title": "Olstein Capital Management, L.P. Buys Generac Holdings Inc, Mastercard Inc, Medtronic PLC, ...",
                "description": "Purchase, NY, based Investment company Olstein Capital Management, L.P. (Current Portfolio) buys Generac Holdings Inc, Mastercard Inc, Medtronic PLC, Zimmer Biomet Holdings Inc, Visa Inc, sells Dollar Tree Inc, Lowe's Inc, CVS Health Corp, WESCO International Inc, Equifax Inc during the 3-months ended 2021Q4, according to the most recent filings of the investment company, Olstein Capital Management, L.P..",
                "publish_date": "2022-01-27T23:38:01Z",
                "link": "https://finance.yahoo.com/news/olstein-capital-management-l-p-233801151.html?.tsrc=rss"
            },
            {
                "guid": "376df2f6-48c5-377d-9dcc-dcc0790c815d",
                "symbol_type": "AAPL",
                "title": "Apple Posts Record Quarterly Results Despite Parts Shortages",
                "description": "Apple posted record quarterly results even as supply shortages hindered sales, and Chief Executive Tim Cook said those constraints are improving.",
                "publish_date": "2022-01-27T23:35:00Z",
                "link": "https://finance.yahoo.com/m/376df2f6-48c5-377d-9dcc-dcc0790c815d/apple-posts-record-quarterly.html?.tsrc=rss"
            },
            {
                "guid": "c4b3aeec-1247-3c41-b1a7-3e5b452844cf",
                "symbol_type": "AAPL",
                "title": "Apple CEO: ‘We Don’t Make Purely Financial Decisions’ About Apple TV Plus Content",
                "description": "Apple has spent untold millions on original content for Apple TV Plus. And CEO Tim Cook acknowledged that it isn’t necessarily looking for a financial payback on that investment. “We don’t make purely financial decisions about the content. We try to find great content that has a reason for being,” he said on Apple’s quarterly […]",
                "publish_date": "2022-01-27T23:08:19Z",
                "link": "https://variety.com/2022/digital/news/apple-tv-plus-purely-financial-decisions-ceo-tim-cook-1235165656/?.tsrc=rss"
            },
            {
                "guid": "d617be54-fce8-3676-98e9-163cdacd173c",
                "symbol_type": "AAPL",
                "title": "Apple's Q1 Surprises to the Upside, Visa Also Beats",
                "description": "Having sold $71.6 billion in iPhones in the past quarter is an admirable feat in any market condition, but fairly extraordinary considering current shortages in microchips.",
                "publish_date": "2022-01-27T23:00:11Z",
                "link": "https://finance.yahoo.com/news/apples-q1-surprises-upside-visa-230011886.html?.tsrc=rss"
            },
            {
                "guid": "f7f4f0a1-3652-3235-957e-00deb9339c6f",
                "symbol_type": "AAPL",
                "title": "Apple (AAPL) Tops Q1 Earnings and Revenue Estimates",
                "description": "Apple (AAPL) delivered earnings and revenue surprises of 11.11% and 4.92%, respectively, for the quarter ended December 2021. Do the numbers hold clues to what lies ahead for the stock?",
                "publish_date": "2022-01-27T22:45:10Z",
                "link": "https://finance.yahoo.com/news/apple-aapl-tops-q1-earnings-224510954.html?.tsrc=rss"
            },
            {
                "guid": "08f9852a-cf0d-3c45-a3bc-15112018f0fe",
                "symbol_type": "AAPL",
                "title": "Livingston Group Asset Management CO (operating as Buys Blackstone Inc, Microsoft Corp, ...",
                "description": "Investment company Livingston Group Asset Management CO (operating as (Current Portfolio) buys Blackstone Inc, Microsoft Corp, Advanced Micro Devices Inc, Nutrien, NVIDIA Corp, sells The Home Depot Inc, Vanguard Information Technology ETF, Cardinal Health Inc, Boswell (JG) Co, Vanguard Mega Cap Value ETF during the 3-months ended 2021Q4, according to the most recent filings of the investment company, Livingston Group Asset Management CO (operating as.",
                "publish_date": "2022-01-27T22:38:25Z",
                "link": "https://finance.yahoo.com/news/livingston-group-asset-management-co-223825127.html?.tsrc=rss"
            },
            {
                "guid": "c54903cb-fe0a-3e05-94ba-554a699e50a9",
                "symbol_type": "AAPL",
                "title": "Bordeaux Wealth Advisors LLC Buys Upstart Holdings Inc, Apple Inc, iShares Core S&P 500 ...",
                "description": "Investment company Bordeaux Wealth Advisors LLC (Current Portfolio) buys Upstart Holdings Inc, Apple Inc, iShares Core S&P 500 ETF, Technology Select Sector SPDR ETF, Vanguard Real Estate Index Fund ETF, sells Focus Financial Partners Inc, Medallia Inc, Vanguard Growth ETF, Alibaba Group Holding, The Walt Disney Co during the 3-months ended 2021Q4, according to the most recent filings of the investment company, Bordeaux Wealth Advisors LLC.",
                "publish_date": "2022-01-27T22:38:13Z",
                "link": "https://finance.yahoo.com/news/bordeaux-wealth-advisors-llc-buys-223813887.html?.tsrc=rss"
            },
            {
                "guid": "a9e73f48-cc2f-3e2c-86e4-3c2eb099d42a",
                "symbol_type": "AAPL",
                "title": "Apple reports blowout earnings, record revenue",
                "description": "Yahoo Finance’s Jared Blikre breaks down the latest Apple earnings report.",
                "publish_date": "2022-01-27T22:22:07Z",
                "link": "https://finance.yahoo.com/video/apple-reports-blowout-earnings-record-222207611.html?.tsrc=rss"
            }
        ]
    }

    def test_ok_response_without_query(self):

        parsed_res = handle_pagination_response(TestPaginationHandler.PAGINATION_TEST_1)

        self.assertEqual(parsed_res['metadata']['page_number'], 1)
        self.assertEqual(parsed_res['metadata']['total_record_count'], 100)
        self.assertEqual(parsed_res['metadata']['page_size'], settings.REST_FRAMEWORK.get('PAGE_SIZE'))
        self.assertEqual(parsed_res['metadata']['total_pages'], 100//settings.REST_FRAMEWORK.get('PAGE_SIZE'))
        self.assertEqual(parsed_res['metadata']['links']['next'], TestPaginationHandler.PAGINATION_TEST_1['next'])
        self.assertEqual(parsed_res['metadata']['links']['previous'],
                         TestPaginationHandler.PAGINATION_TEST_1['previous'])

        self.assertEqual(len(parsed_res['records']), len(TestPaginationHandler.PAGINATION_TEST_1['results']))

    def test_empty_response_without_query(self):

        parsed_res = handle_pagination_response(TestPaginationHandler.PAGINATION_TEST_2)

        self.assertEqual(parsed_res['metadata']['page_number'], 1)
        self.assertEqual(parsed_res['metadata']['total_record_count'], 0)
        self.assertEqual(parsed_res['metadata']['page_size'], settings.REST_FRAMEWORK.get('PAGE_SIZE'))
        self.assertEqual(parsed_res['metadata']['total_pages'], 1)
        self.assertEqual(parsed_res['metadata']['links']['next'], None)
        self.assertEqual(parsed_res['metadata']['links']['previous'], None)

        self.assertEqual(len(parsed_res['records']), 0)

    def test_ok_response_with_ok_query(self):
        page_number = 2
        parsed_res = handle_pagination_response(TestPaginationHandler.PAGINATION_TEST_3, page_number)

        self.assertEqual(parsed_res['metadata']['page_number'], 2)
        self.assertEqual(parsed_res['metadata']['total_record_count'], 52)
        self.assertEqual(parsed_res['metadata']['page_size'], settings.REST_FRAMEWORK.get('PAGE_SIZE'))
        self.assertEqual(parsed_res['metadata']['total_pages'], 6)
        self.assertEqual(parsed_res['metadata']['links']['next'], TestPaginationHandler.PAGINATION_TEST_3['next'])
        self.assertEqual(parsed_res['metadata']['links']['previous'],
                         TestPaginationHandler.PAGINATION_TEST_3['previous'])

        self.assertEqual(len(parsed_res['records']), len(TestPaginationHandler.PAGINATION_TEST_3['results']))


