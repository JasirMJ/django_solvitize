from .models import ErrorModel
from django_solvitize.utils.DynamicFieldsModel import DynamicFieldsModelSerializer
from .models import *

class ErrorAppSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = ErrorModel
        # fields = ["mobile_number", "whatsapp_number", "is_customer", "is_staff"]
        fields = "__all__"

class ErrorAppDropdownSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = ErrorModel
        fields = ["id", "name"]



