from django.db import models


class JobListing(models.Model):
    title = models.CharField(max_length=55)
    description = models.TextField()
    company = models.ForeignKey("JobifyUser", on_delete=models.CASCADE)
    interested = models.ManyToManyField("JobifyUser", through="JobListingUser", related_name="interested")