# Generated by Django 3.2.7 on 2021-10-03 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_post_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='like',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(blank=True),
        ),
    ]
