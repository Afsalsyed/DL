# dl/models
from django.db import models
from oss.models import Journal, Accepted_Submission

# Create your models here.


class Volume(models.Model):
    volume = models.IntegerField()
    description = models.CharField(max_length=255, null=True, blank=True)
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


class Published_article(models.Model):
    accepted_submission = models.ForeignKey(Accepted_Submission, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    published_on_date = models.DateField()
    doi = models.CharField(max_length=255)