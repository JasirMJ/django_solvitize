from django.db import models

# Create your models here.
class ErrorModel(models.Model):
    title = models.CharField(null=False,max_length=255)
    body = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    data = models.TextField(null=True)