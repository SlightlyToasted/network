# Generated by Django 5.0.6 on 2024-08-03 02:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_alter_user_followers_alter_user_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes_users',
            field=models.ManyToManyField(null=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
