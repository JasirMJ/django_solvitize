from django.contrib import admin
from .models import APIRequestResponseLog

# Register your models here.
class APIRequestResponseLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'method', 'response_status', 'created_at', 'updated_at',)
    search_fields = ('method', 'response_status',)
    list_filter = ('method',)


admin.site.register(APIRequestResponseLog, APIRequestResponseLogAdmin)
