# Generated by Django 3.1.7 on 2021-04-20 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Job', '0015_businessandstudent_jid'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='email',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='major',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
