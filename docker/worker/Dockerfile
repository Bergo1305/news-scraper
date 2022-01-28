FROM bergo1305/news-base:latest

RUN echo "Creating application folder ..."
RUN mkdir /app

RUN pip3 install --user redis==4.1.1
RUN pip3 install xmltodict==0.12.0

COPY news_scraper/ /app/news_scraper
COPY docker/worker/entrypoint.sh /app
COPY manage.py /app
WORKDIR /app

RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

