# Generated by Django 5.1.4 on 2025-01-02 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_alter_book_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='name',
            field=models.CharField(max_length=120, verbose_name='name'),
        ),
    ]
