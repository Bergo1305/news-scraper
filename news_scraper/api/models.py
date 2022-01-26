from django.db import models


class News(models.Model):

    guid = models.CharField(max_length=40)
    symbol_type = models.CharField(max_length=100)
    title = models.TextField()
    description = models.TextField()
    publish_date = models.DateTimeField()
    link = models.TextField()

