# Generated by Django 5.1.4 on 2025-01-06 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salespersons', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesperson',
            name='pic',
            field=models.ImageField(default='no_picture.jpg', upload_to='customers'),
        ),
    ]
