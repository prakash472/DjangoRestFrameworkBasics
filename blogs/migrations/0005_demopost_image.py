# Generated by Django 3.1.3 on 2020-12-20 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0004_categories_demopost'),
    ]

    operations = [
        migrations.AddField(
            model_name='demopost',
            name='image',
            field=models.TextField(default='post_1.jpg'),
        ),
    ]