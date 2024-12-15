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
                FIREBASE_AUTHENTICATE_API, params={"key": FIREBASE_WEB_API_KEY}, json={"idToken": id_token},
            )

            # Log Firebase response status code and data
            api_log.api_response_data = response.text
            api_log.response_status = response.status_code
            api_log.save()

            if response.status_code == 200:
                firebase_data = response.json()
                if "users" in firebase_data and len(firebase_data["users"]) > 0:
                    user_data = firebase_data["users"][0]
                    formatted_response = FirebaseUserLookupResponseSerializer(user_data).data
                    return ResponseFunction(1, "Successfully fetched all data.", formatted_response)
                else:
                    return ResponseFunction(0, 'User not found.', {})
            else:
                return ResponseFunction(0, 'Error occured in Firebase Api.', {})
        except requests.RequestException:
            api_log.api_response_data = str({"error": "Failed to connect to Firebase"})
            api_log.response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            api_log.save()
            return ResponseFunction(0, 'Failed to connect to Firebase.', {})

    