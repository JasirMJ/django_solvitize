import requests
from rest_framework.views import APIView
from rest_framework import status
from firebase_admin import messaging

from .serializers import FirebaseUserLookupRequestSerializer, FirebaseUserLookupResponseSerializer
from django_solvitize.utils.GlobalFunctions import *
from django_solvitize.utils.constants import *
from .models import APIRequestResponseLog
from .notifications.notifications import send_notification, subscribe_or_unsubscribe_topic



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
        


class SendNotificationView(APIView):
    """
    API endpoint to send push notifications to users.
    """
    def post(self, request):
        print("Post Notification to user ", request.data)
        token = request.data.get("token")  # Device FCM token
        title = request.data.get("title")  # Notification title
        body = request.data.get("body")  # Notification body
        image = request.data.get("image")  # Notification image
        data = request.data.get("data", {})  # Optional additional data

        # if not token or not title or not body:
        #     return Response(
        #         {"error": "Token, title, and body are required."},
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )
        
        response = send_notification(token, title, image, body, 'token', data)
        print(response)
        
        return Response({"message": "Notification sent.", "response": response}, status=status.HTTP_200_OK)

class SendTopicNotificationView(APIView):
    """
    API endpoint to send push notifications to a topic.
    """
    def post(self, request):
        print("Post Notification to topic ", request.data)
        
        topic = request.data.get("topic", "global")  # Default topic is 'global'
        title = request.data.get("title")
        image = request.data.get("image")
        body = request.data.get("body")
        data = request.data.get("data", {})

        if not title or not body:
            return Response(
                {"error": "Title and body are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = send_notification(topic, title,image, body, 'topic', data)
        return Response({"message": "Notification sent.", "response": response}, status=status.HTTP_200_OK)
    
    
class SubscribeTopicView(APIView):
    def post(self, request):
        fcm_token = request.data.get("fcm_token") 
        topic_name = request.data.get("topic_name")
        
        # return Response(
        #     "topic_name: " + topic_name + " fcm_token: " + fcm_token
        # )
        if not fcm_token or not topic_name:
            return Response({"error": "FCM token and topic name are required."}, status=status.HTTP_400_BAD_REQUEST)

        response = subscribe_or_unsubscribe_topic('suscribe', fcm_token, topic_name)
        return Response(response, status=status.HTTP_200_OK)
    

class UnsubscribeTopicView(APIView):
    def post(self, request):
        fcm_token = request.data.get("fcm_token")
        topic_name = request.data.get("topic_name")

        if not fcm_token or not topic_name:
            return Response({"error": "FCM token and topic name are required."}, status=status.HTTP_400_BAD_REQUEST)

        response = subscribe_or_unsubscribe_topic('unsuscribe', fcm_token, topic_name)
        return Response(response, status=status.HTTP_200_OK)

