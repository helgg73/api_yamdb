# Generated by Django 3.2 on 2023-03-18 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='reviews',
            constraint=models.UniqueConstraint(fields=('title', 'author'), name='unique_review_from_author'),
        ),
    ]
