# Generated by Django 3.2 on 2023-03-18 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_reviews_unique_review_from_author'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='reviews',
            name='unique_review_from_author',
        ),
    ]