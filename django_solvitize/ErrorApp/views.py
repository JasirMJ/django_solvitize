from django.shortcuts import render

# Create your views here.
from .models import *
from .serializers import ErrorAppSerializer, ErrorAppDropdownSerializer
from django_solvitize.utils.functions import *
from django_solvitize.utils.GlobalImports import *



class ErrorAppAPI(ListAPIView):

    serializer_class = ErrorAppSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        pagination = self.request.GET.get('pagination', '1')
        if pagination == '0':
            print("Pagination None")
            self.pagination_class = None

        id = self.request.GET.get('id', '')
        name = self.request.GET.get('name', '')
        is_dropdown = self.request.GET.get('is_dropdown', False)

        if is_dropdown=='1':
            print("Drop down get request")
            self.serializer_class = ErrorAppDropdownSerializer

        qs = ErrorModel.objects.all()

        if id:
            qs = qs.filter(id=id)
        if name:
            qs = qs.filter(name__icontains=name)
        return qs

    def post(self, request):
        required = ["name"]
        validation_errors = ValidateRequest(required, self.request.data)

        if len(validation_errors) > 0:
            return ResponseFunction(0, validation_errors[0]['error'],{})
        else:
            print("Receved required Fields")
        try:
            id = self.request.POST.get("id", "")

            if id:
                print("ErrorApp Updating")
                store_qs = ErrorModel.objects.filter(id=id)
                if not store_qs.count():
                    return ResponseFunction(0, "ErrorApp Not Found", {})
                variant_obj = store_qs.first()
                serializer = ErrorAppSerializer(variant_obj, data=request.data, partial=True)
                msg = "Data updated"
            else:
                print("Adding new ErrorApp")
                serializer = ErrorAppSerializer(data=request.data, partial=True)
                msg = "Data saved"
            serializer.is_valid(raise_exception=True)

            obj = serializer.save()

            return ResponseFunction(1, msg, ErrorAppSerializer(obj).data)
        except Exception as e:
            printLineNo()

            print("Excepction ", printLineNo(), " : ", e)
            # print("Excepction ",type(e))

            return ResponseFunction(0,f"Excepction occured {str(e)}",{})

    def delete(self, request):
        try:
            id = self.request.GET.get('id', "[]")
            if id == "all":

                ErrorModel.objects.all().delete()
                return ResponseFunction(1, "Deleted all data",{})

            else:
                id = json.loads(id)
                # print(id)
                ErrorModel.objects.filter(id__in=id).delete()
                return ResponseFunction(1, "Deleted data having id " + str(id),{})

        except Exception as e:
            printLineNo()

            return Response(
                {
                    STATUS: False,
                    MESSAGE: str(e),
                    "line_no": printLineNo()
                }
            )

