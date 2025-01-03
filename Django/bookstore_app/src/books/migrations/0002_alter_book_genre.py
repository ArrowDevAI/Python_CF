# Generated by Django 5.1.4 on 2025-01-02 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.CharField(choices=[('classic', 'Classic'), ('romantic', 'Romantic'), ('comic', 'Comic'), ('fantasy', 'Fantasy'), ('horror', 'Horror'), ('educational', 'Educational'), ('sci-fi', 'Sci-Fi')], default='classic', max_length=12),
        ),
    ]