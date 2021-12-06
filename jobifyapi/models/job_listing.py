from django.db import models


class JobListing(models.Model):
    title = models.ForeignKey("Title", on_delete=models.CASCADE)
    description = models.TextField()
    company = models.ForeignKey("JobifyUser", on_delete=models.CASCADE)
    interested = models.ManyToManyField("JobifyUser", through="JobListing-User", related_name="interested")