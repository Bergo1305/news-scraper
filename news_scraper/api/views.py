import json
import math
from django.http import Http404, HttpResponseBadRequest, HttpResponse, HttpResponseServerError
from django.conf import settings
from news_scraper.settings import SYMBOL_TYPES
from news_scraper.api.models import News
from news_scraper.api.serializers import NewsSerializer
from news_scraper.logger import LOGGER
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view


class LimitSetPagination(PageNumberPagination):
    page_size_query_param = settings.REST_FRAMEWORK.get('PAGE_SIZE_QUERY_PARAM')
    max_page_size = settings.REST_FRAMEWORK.get('MAX_PAGE_SIZE')


def handle_pagination_response(pagination_res, page_num=None, limit=None):

    if page_num is None:
        page_num = 1
    else:
        page_num = int(page_num)

    if limit is not None:
        limit = int(limit)

    total_record_count = pagination_res.get('count', 0)
    page_size = settings.REST_FRAMEWORK.get('PAGE_SIZE')
    total_pages = math.ceil(total_record_count / page_size) if limit is None else math.ceil(
        total_record_count / limit)
    page_size = page_size if limit is None else limit

    return {
        "metadata": {
            "page_number": page_num,
            "total_record_count": total_record_count,
            "page_size": page_size,
            "total_pages": total_pages if total_pages != 0 else 1,
            "links": {
                "next": pagination_res.get('next'),
                "previous": pagination_res.get('previous')
            }
        },
        "records": pagination_res.get('results', [])
    }


@api_view(['GET', ])
def news(request):
    symbol_type = request.GET.get('s', None)

    if symbol_type is None:
        return HttpResponseBadRequest(
            json.dumps({"error_msg": "Query parameter 's' is required. (Example s=AAPL)"}),
            content_type='application/json'
        )

    if symbol_type not in SYMBOL_TYPES:
        return HttpResponseBadRequest(
            json.dumps({"error_msg": f"Query parameter s='{symbol_type}' is not currently supported."}),
            content_type='application/json'
        )

    try:
        query = News.objects.filter(symbol_type=symbol_type).order_by('-publish_date')
    except Exception as _exc:
        LOGGER.exception(f"Problem with fetching data with request: {request}")
        LOGGER.exception(f"Reason: {_exc}")
        return Http404

    news_paginator = LimitSetPagination()
    results = news_paginator.paginate_queryset(query, request)
    serializer = NewsSerializer(results, many=True)

    pagination = news_paginator.get_paginated_response(serializer.data)
    pagination_res = dict(pagination.data)

    page_num = request.GET.get('page', None)
    limit = request.GET.get(settings.REST_FRAMEWORK.get('PAGE_SIZE_QUERY_PARAM'), None)

    res = handle_pagination_response(pagination_res, page_num, limit)
    return HttpResponse(
        json.dumps(res),
        content_type='application/json'
    )




