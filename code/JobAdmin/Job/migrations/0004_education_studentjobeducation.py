# Generated by Django 3.1.7 on 2021-03-31 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Job', '0003_auto_20210330_1020'),
    ]

    operations = [
        migrations.CreateModel(
            name='Education',
            fields=[
                ('eid', models.AutoField(primary_key=True, serialize=False)),
                ('education', models.CharField(max_length=255)),
                ('major', models.CharField(max_length=255)),
                ('university', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'Education',
                'ordering': ['eid'],
            },
        ),
        migrations.CreateModel(
            name='StudentJobEducation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sid', models.IntegerField(null=True)),
                ('jid', models.IntegerField(null=True)),
                ('eid', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'StudentJobEducation',
                'ordering': ['id'],
            },
        ),
    ]