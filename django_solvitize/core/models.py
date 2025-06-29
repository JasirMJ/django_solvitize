from django.db import models

# Create your models here.
class AbstractDateBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,
                                      help_text='Date and time when the '
                                                'entry was created')
    updated_at = models.DateTimeField(auto_now=True,
                                       help_text='Date and time when the '
                                                 'entry was updated')

    class Meta:
        abstract = True
