from django.db import models

class JobListingUser(models.Model):
    jobify_user = models.ForeignKey("JobifyUser", on_delete=models.CASCADE)
    job_listing = models.ForeignKey("JobListing", on_delete=models.CASCADE)