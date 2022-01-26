FROM bergo1305/news-base:latest

RUN echo "Creating application folder ..."
RUN mkdir /app

RUN pip3 install xmltodict==0.12.0

COPY news_scraper/ /app/news_scraper
COPY manage.py /app
COPY docker/api/entrypoint.sh /app

RUN mkdir /app/data
WORKDIR /app

RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

