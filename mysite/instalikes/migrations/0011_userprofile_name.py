# Generated by Django 3.0.4 on 2020-05-22 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instalikes', '0010_date_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='name',
            field=models.CharField(default='', max_length=225),
        ),
    ]