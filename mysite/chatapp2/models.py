from django.db import models

# Create your models here.
class usersidle(models.Model):
    name = models.CharField(max_length=220)
    roomid = models.CharField(max_length=330)

