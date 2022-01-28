import django.contrib.postgres.indexes
from django.db import migrations, models
from django.contrib.postgres.operations import AddIndexConcurrently


class Migration(migrations.Migration):

    atomic = False

    dependencies = [
        ('api', '0001_initial')
    ]

    operations = [
        AddIndexConcurrently(
            model_name="news",
            index=models.Index(
                fields=['guid'], name="guid_news_idx"
            )
        )
    ]
