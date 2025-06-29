
import requests
from django_solvitize.firebase.models import APIRequestResponseLog
from django_solvitize.firebase.serializers import FirebaseUserLookupResponseSerializer
from django_solvitize.utils.constants import FIREBASE_AUTHENTICATE_API
from rest_framework import status


def google_login_verify(request_data, api_key, id_token):
        try:
            response_status = None
            status_code = None
            message = ""
            response_data = {}
            formatted_response = {}

            api_log = APIRequestResponseLog.objects.create(
                method='POST',
                api_request_data=str(request_data),
                response_status=None,
            )
            response = requests.post(
                FIREBASE_AUTHENTICATE_API, params={"key": api_key}, json={"idToken": id_token},
            )
            # Log Firebase response status code and data
            status_code = response.status_code
            print("Firebase api response: ", response.text)

            if status_code == status.HTTP_200_OK:
                firebase_data = response.json()
                if "users" in firebase_data and len(firebase_data["users"]) > 0:
                    user_data = firebase_data["users"][0]
                    formatted_response = FirebaseUserLookupResponseSerializer(
                        user_data).data

                    if user_data.get('emailVerified', False):
                        message = "Firebase google verification is successfull."
                    else:
                        message = "Firebase phone verification is successfull."
                    response_status = True
                else:
                    message = 'User not found.'
                    response_status = False              
                    
                response_data = {
                    "status": response_status,
                    "message": message,
                    "data": formatted_response
                }
                return response_data
            else:
                status_code = response.status_code
                try:
                    api_response_data = response.json()
                    if "error" in api_response_data:
                        message = api_response_data["error"].get("message")
                    else:
                        message = f"Unknown error format in response: {response.text}"
                        
                except ValueError:
                    message = f"Failed to parse response as JSON: {response.text}"
                
                response_status = False
                response_data = {
                    "status": response_status,
                    "message": message,
                    "data": formatted_response
                }
                
            return response_data

        except requests.RequestException:
            message = "Failed to connect to Firebase."
            response_data = {
                "status": False,
                "message": message,
                "data": formatted_response
            }
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            return response_data
        except Exception as e:
            message = str(e)
            response_data = {
                "status": False,
                "message": message,
                "data": formatted_response
            }
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            return response_data
            
        finally:
            api_log.api_response_data = str(response_data)
            api_log.response_status = status_code
            api_log.save()