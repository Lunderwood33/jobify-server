from django.db import models


class JobListing(models.Model):
    title = models.CharField(max_length=55)
    description = models.TextField()
    wage = models.IntegerField()
    company = models.ForeignKey("JobifyUser", on_delete=models.CASCADE)
    job_type = models.ForeignKey("JobType", on_delete=models.CASCADE)
    interested = models.ManyToManyField("JobifyUser", through="JobListingUser", related_name="interested")
    url = models.CharField(max_length=150)