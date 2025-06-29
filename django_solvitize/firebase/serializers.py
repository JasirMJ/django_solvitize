from rest_framework import serializers

class FirebaseUserLookupRequestSerializer(serializers.Serializer):
    """
    Validates the request payload for the Firebase User Lookup API
    """
    idToken = serializers.CharField(max_length=5000, required=True)


class FirebaseUserLookupResponseSerializer(serializers.Serializer):
    """
    Formats the response for the Firebase User Lookup API
    """
    localId = serializers.CharField(max_length=255)
    email = serializers.EmailField(required=False)
    phoneNumber = serializers.CharField(max_length=15, required=False)
    displayName = serializers.CharField(max_length=255, required=False)
    photoUrl = serializers.URLField(required=False)
    emailVerified = serializers.BooleanField(default=False)
    lastLoginAt = serializers.CharField(required=False)
    createdAt = serializers.CharField(required=False)
