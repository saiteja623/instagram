# Generated by Django 3.0.4 on 2020-04-22 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(max_length=225, upload_to='')),
                ('likes', models.IntegerField(max_length=10000)),
            ],
        ),
    ]