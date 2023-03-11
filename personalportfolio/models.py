from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Skills(models.Model):
    class Meta:
        verbose_name_plural = "skills"
        verbose_name = 'skill'

    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField()
    image = models.FileField(blank=True, null=True, upload_to="images")

    def __str__(self):
        return f"{self.name}"

class Contact(models.Model):
    class Meta:
        verbose_name_plural = "contacts"
        verbose_name = "contact"
    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    subject = models.CharField(max_length=100, blan=True, null=True )
    message = models.TextField()

    def __str__(self):
        return f"{self.subject}"
