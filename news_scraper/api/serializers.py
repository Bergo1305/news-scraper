from rest_framework import serializers
from .models import News


class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = ('guid', 'symbol_type', 'title', 'description', 'publish_date', 'link')
