# Generated by Django 5.0.7 on 2024-07-21 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]