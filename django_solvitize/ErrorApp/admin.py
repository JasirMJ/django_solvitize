from django.contrib import admin

# Register your models here.

from .models import *


class ErrorModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'body', 'created_at', 'updated_at', 'data')
    search_fields = ('title', 'body', 'data')
    list_filter = ('created_at', 'updated_at')


admin.site.register(ErrorModel, ErrorModelAdmin)
