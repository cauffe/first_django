from django.db import models

# Create your models here.
class State(models.Model):
    abbreviation = models.CharField(max_length=2)
    name = models.CharField(max_length=100, unique=True)
    capital = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
	population = models.IntegerField()

    def __unicode__(self):
        return self.name


