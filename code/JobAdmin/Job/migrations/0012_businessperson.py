# Generated by Django 3.1.7 on 2021-04-15 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Job', '0011_job_bid'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessPerson',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('bno', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('dept', models.CharField(max_length=255)),
                ('bid', models.IntegerField()),
            ],
            options={
                'db_table': 'BusinessPerson',
                'ordering': ['id'],
            },
        ),
    ]
