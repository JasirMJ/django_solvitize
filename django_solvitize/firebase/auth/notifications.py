from firebase_admin import messaging, credentials
import firebase_admin 


def send_notification(notification_data, title, image, body, notification_type, data=None):
    """
    Sends a push notification to a specific device or topic.

    :param notification_data: FCM device token or Firebase topic name (e.g., 'global')
    :param title: Notification title
    :param image: Notification image URL
    :param body: Notification body
    :param notification_type: Either 'topic' or 'token' to specify the type of notification
    :param data: Additional data as a dictionary (optional)
    :return: Response from Firebase or error message
    """
    try:
        notification = messaging.Notification(title=title, body=body, image=image)
        message_data = {
            "notification": notification,
            "data": data or {},
        }

        if notification_type == 'topic':
            message = messaging.Message(**message_data, topic=notification_data)
        elif notification_type == 'token':
            message = messaging.Message(
                **message_data,
                token=notification_data,
                apns=messaging.APNSConfig(
                    # headers={
                    #     "apns-priority": "10",  # High priority
                    # },
                    # payload=messaging.APNSPayload(
                    #     aps=messaging.Aps(
                    #         alert="This is an iOS-specific alert.",
                    #         badge=1
                    #     )
                    # )
                ),  # Add APNS configurations if needed
                android=messaging.AndroidConfig(
                    # """
                    # Android-specific options that can be included in a message.

                    # Args:
                    #     collapse_key: Collapse key string for the message (optional). This is an identifier for a
                    #         group of messages that can be collapsed, so that only the last message is sent when delivery can be resumed. A maximum of 4 different collapse keys may be active at a given time.
                    #     priority: Priority of the message (optional). Must be one of high or normal.
                    #     ttl: The time-to-live duration of the message (optional). This can be specified
                    #         as a numeric seconds value or a datetime.timedelta instance.
                    #     restricted_package_name: The package name of the application where the registration tokens
                    #         must match in order to receive the message (optional).
                    #     data: A dictionary of data fields (optional). All keys and values in the dictionary must be
                    #         strings. When specified, overrides any data fields set via Message.data.
                    #     notification: A messaging.AndroidNotification to be included in the message (optional).
                    #     fcm_options: A messaging.AndroidFCMOptions to be included in the message (optional).
                    #     direct_boot_ok: A boolean indicating whether messages will be allowed to be delivered to
                    #         the app while the device is in direct boot mode (optional).
                    # """
                        # priority="high",
                        # ttl=86400
                ),  # Add Android configurations if needed
                webpush=messaging.WebpushConfig(
                    # Webpush-specific options that can be included in a message.

                    # Args:
                    # headers: A dictionary of headers (optional). Refer Webpush Specification_ for supported
                    # headers.
                    # data: A dictionary of data fields (optional). All keys and values in the dictionary must be
                    # strings. When specified, overrides any data fields set via Message.data.
                    # notification: A messaging.WebpushNotification to be included in the message (optional).
                    # fcm_options: A messaging.WebpushFCMOptions instance to be included in the message
                    # (optional).
                ),  # Add Webpush configurations if needed
            )
        else:
            return None

        response = messaging.send(message)
        return response
    except Exception as e:
        return str(e)
    

def subscribe_or_unsubscribe_topic(optn_type, fcm_token, topic_name):
    try:
        if optn_type == 'subscribe':
             response = messaging.subscribe_to_topic([fcm_token], topic_name)
             message = "Subscribed successfully"
        else:
            response = messaging.unsubscribe_from_topic([fcm_token], topic_name)
            message = "Unsubscribed successfully"

        response_data = {
            "success_count": response.success_count,
            "failure_count": response.failure_count,
            "errors": [error.reason for error in response.errors],  # Extract error reasons if any
        }
        print(f"Successfully subscribed to {topic_name}: {response_data}")
        return {"message": message, "response": response_data}
    except Exception as e:
        print(f"Errorsubscribing or unsubscribing from topic {topic_name}: {e}")
        return {"error": str(e)}
    

def initialise_firebase_sdk(file_path):
    if not firebase_admin._apps:
        cred = credentials.Certificate(file_path)
        firebase_admin.initialize_app(cred)
        print("Firebase Admin SDK initialized")
    else:
        print("Firebase Admin SDK already initialized")
