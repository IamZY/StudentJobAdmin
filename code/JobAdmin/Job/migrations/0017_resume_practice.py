# Generated by Django 3.1.7 on 2021-04-20 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Job', '0016_auto_20210420_0845'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='practice',
            field=models.TextField(null=True),
        ),
    ]