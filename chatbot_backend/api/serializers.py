from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ChatMessage

# PUBLIC_INTERFACE
class ChatMessageSerializer(serializers.ModelSerializer):
    """
    Serializes ChatMessage for API usage.
    """
    class Meta:
        model = ChatMessage
        fields = ['id', 'user', 'message', 'response', 'timestamp']
        read_only_fields = ['id', 'user', 'response', 'timestamp']

class ChatMessageHistorySerializer(serializers.ModelSerializer):
    """
    Serializes ChatMessage for chat history display.
    """
    user = serializers.StringRelatedField()

    class Meta:
        model = ChatMessage
        fields = ['id', 'user', 'message', 'response', 'timestamp']

# PUBLIC_INTERFACE
class UserSerializer(serializers.ModelSerializer):
    """
    Serializes User for authentication endpoints.
    """
    class Meta:
        model = User
        fields = ['id', 'username']
