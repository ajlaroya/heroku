# Generated by Django 3.2.7 on 2021-10-09 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_remove_post_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='colour',
            field=models.CharField(default='#ffffff', max_length=7),
        ),
    ]