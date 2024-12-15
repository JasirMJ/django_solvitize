import requests
from rest_framework.views import APIView
from rest_framework import status

from .serializers import FirebaseUserLookupRequestSerializer, FirebaseUserLookupResponseSerializer
from django_solvitize.utils.GlobalFunctions import *
from django_solvitize.utils.constants import *
from .models import APIRequestResponseLog



class FirebaseUserLookupView(APIView):
    """
    Handles Firebase User Lookup using the accounts:lookup API
    """

    def post(self, request):
        
        request_data = request.data
        serializer = FirebaseUserLookupRequestSerializer(data=request.data)
        api_key = request.headers.get("Api-Key")

        if not serializer.is_valid():
            return ResponseFunction(0, serializer.errors,{})

        api_log = APIRequestResponseLog.objects.create(
            method='POST',
            api_request_data=str(request_data),
            response_status=None,
        )
        id_token = serializer.validated_data["idToken"]
        try:
            response = requests.post(
                FIREBASE_AUTHENTICATE_API, params={"key": api_key}, json={"idToken": id_token},
            )
            # Log Firebase response status code and data
            api_log.response_status = response.status_code
            print("Firebase api response: ", response.text)

            if response.status_code == 200:
                firebase_data = response.json()
                if "users" in firebase_data and len(firebase_data["users"]) > 0:
                    user_data = firebase_data["users"][0]
                    formatted_response = FirebaseUserLookupResponseSerializer(user_data).data

                    if user_data.get('emailVerified', False):
                        message = "Firebase google verification is successfull."
                    else:
                        message = "Firebase phone verification is successfull."

                    response_data = {
                        "status": True,
                        "message": message
                    }
                    api_log.api_response_data = str(response_data)
                    api_log.save()
                    return ResponseFunction(1, message, formatted_response)
                else:
                    message = 'User not found.'
                    response_data = {
                            "status": False,
                            "message": message
                        }
                    api_log.api_response_data = str(response_data)
                    api_log.save()

                    return ResponseFunction(0, message, {})
            else:
                try:
                    api_response_data = response.json()
                    if "error" in api_response_data:
                        message = api_response_data["error"].get("message") 
                        response_data = {
                                    "status": False,
                                    "message": message
                                }
                        api_log.api_response_data = str(response_data)
                        api_log.save()
                    else:
                        print("Unknown error format in response:", response.text)
                except ValueError:
                    print("Failed to parse response as JSON:", response.text)

                return ResponseFunction(0, 'Error occured in Firebase Api.', {})
        except requests.RequestException:
            message = "Failed to connect to Firebase."
            response_data = {
                            "status": False,
                            "message": message
                        }
            api_log.api_response_data = str(response_data)
            api_log.response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            api_log.save()

            return ResponseFunction(0, message, {})
  