from django.db import models
from oss.models import Journal

# Create your models here.


class Volume(models.Model):
    volume = models.IntegerField()
    description = models.CharField(max_length=255)
    year = models.IntegerField()
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.volume)

class Issue(models.Model):
    issue = models.IntegerField()
    volume = models.ForeignKey(Volume, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    

    def __str__(self):
        return str(self.issue)

