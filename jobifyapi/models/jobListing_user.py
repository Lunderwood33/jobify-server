from django.db import models

class JobListingUser(models.Model):
    user = models.ForeignKey("JobifyUser", on_delete=models.CASCADE)
    jobListing = models.ForeignKey("JobListing", on_delete=models.CASCADE)