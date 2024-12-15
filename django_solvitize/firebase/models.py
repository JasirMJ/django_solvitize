from django.db import models
from django_solvitize.core.models import AbstractDateBase

# Create your models here.
class APIRequestResponseLog(AbstractDateBase):
    method = models.CharField(max_length=10)
    api_request_data = models.TextField(null=True, blank=True)
    api_response_data = models.TextField(null=True, blank=True)
    response_status = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.method} - {self.response_status}"
    
    class Meta:
        verbose_name = "API Request-Response Log"
