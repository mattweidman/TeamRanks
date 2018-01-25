from django.db import models

class Preference(models.Model):
    prefid = models.CharField(max_length=256, primary_key=True)
    user = models.CharField(max_length=256)
    choice = models.CharField(max_length=256)
    weight = models.FloatField(default=0)
