# Generated by Django 5.1.4 on 2025-01-05 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booksapp', '0003_alter_book_image_reviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='is_borrowed',
            field=models.BooleanField(default=False),
        ),
    ]
