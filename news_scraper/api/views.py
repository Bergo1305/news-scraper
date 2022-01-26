from django.http import Http404, HttpResponseBadRequest
from django.conf import settings
from news_scraper.settings import SYMBOL_TYPES
from news_scraper.api.models import News
from news_scraper.api.serializers import NewsSerializer
from news_scraper.logger import LOGGER
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view


class LimitSetPagination(PageNumberPagination):
    page_size_query_param = settings.REST_FRAMEWORK.get('PAGE_SIZE_QUERY_PARAM', 'limit')
    max_page_size = settings.REST_FRAMEWORK.get('MAX_PAGE_SIZE', 1000)


@api_view(['GET', ])
def news(request):
    symbol_type = request.GET.get('s', None)

    if symbol_type and symbol_type not in SYMBOL_TYPES:
        return HttpResponseBadRequest(f"Symbol type: {symbol_type} currently not supported.")

    if symbol_type is None:
        return HttpResponseBadRequest(f"Symbol (s) query parameter not provided.")

    try:
        query = News.objects.all().order_by('-publish_date') if not symbol_type else \
            News.objects.filter(symbol_type=symbol_type).order_by('-publish_date')
    except Exception as _exc:
        LOGGER.exception(f"Problem with fetching data with request: {request}")
        LOGGER.exception(f"Reason: {_exc}")
        return Http404

    news_paginator = LimitSetPagination()
    results = news_paginator.paginate_queryset(query, request)
    LOGGER.debug(results)
    serializer = NewsSerializer(results, many=True)

    return news_paginator.get_paginated_response(serializer.data)





