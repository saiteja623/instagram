# Generated by Django 3.0.4 on 2020-05-22 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instalikes', '0008_auto_20200520_1400'),
    ]

    operations = [
        migrations.CreateModel(
            name='date',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
