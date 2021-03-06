# Generated by Django 3.1.7 on 2021-04-15 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Job', '0009_auto_20210415_1010'),
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('businessName', models.CharField(max_length=255)),
                ('businessPerson', models.CharField(max_length=255)),
                ('businessType', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'Business',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='BusinessAndStudent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('bid', models.IntegerField()),
                ('rid', models.IntegerField()),
            ],
            options={
                'db_table': 'BusinessAndStudent',
                'ordering': ['id'],
            },
        ),
    ]
