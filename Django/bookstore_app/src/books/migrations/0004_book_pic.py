# Generated by Django 5.1.4 on 2025-01-07 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_alter_book_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='pic',
            field=models.ImageField(default='no_picture.jpg', upload_to='books'),
        ),
    ]
