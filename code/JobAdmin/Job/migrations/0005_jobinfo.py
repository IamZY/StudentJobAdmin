# Generated by Django 3.1.7 on 2021-03-31 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Job', '0004_education_studentjobeducation'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('businessName', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('jobName', models.CharField(max_length=255)),
                ('businessType', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'JobInfo',
                'ordering': ['id'],
            },
        ),
    ]