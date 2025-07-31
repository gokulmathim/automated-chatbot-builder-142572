from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import ChatMessage
from .serializers import ChatMessageSerializer, ChatMessageHistorySerializer, UserSerializer

@api_view(['GET'])
def health(request):
    """Health check endpoint."""
    return Response({"message": "Server is up!"})

# PUBLIC_INTERFACE
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def message(request):
    """
    Receives a chat message, generates automated response, saves to DB, and returns response.
    ---
    request:
      message: string (User's question)
    response:
      id: ID of message
      message: Original user message
      response: Chatbot reply
      timestamp: message sent time
    """
    serializer = ChatMessageSerializer(data=request.data)
    if serializer.is_valid():
        user_message = serializer.validated_data['message']
        # Fake chatbot logic (replace with real in production)
        bot_response = automated_bot_reply(user_message)

        chat_obj = ChatMessage.objects.create(
            user=request.user,
            message=user_message,
            response=bot_response,
        )
        return Response(ChatMessageSerializer(chat_obj).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def automated_bot_reply(user_message):
    # Placeholder - can be replaced with LLM/real chatbot logic
    return f"Echo: {user_message}"

# PUBLIC_INTERFACE
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def history(request):
    """
    Returns chat history for the currently authenticated user.
    ---
    response:
      - List of chat messages
    """
    messages = ChatMessage.objects.filter(user=request.user).order_by('timestamp')
    serializer = ChatMessageHistorySerializer(messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# PUBLIC_INTERFACE
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login endpoint for user authentication.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'detail': 'Login successful', 'user': UserSerializer(user).data})
    return Response({'detail': 'Invalid credentials'}, status=401)

# PUBLIC_INTERFACE
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Register a new user for the chatbot system.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'detail': 'Missing username or password'}, status=400)
    if User.objects.filter(username=username).exists():
        return Response({'detail': 'Username already exists'}, status=400)
    user = User.objects.create_user(username=username, password=password)
    return Response({'detail': 'Registration successful', 'user': UserSerializer(user).data}, status=status.HTTP_201_CREATED)

# PUBLIC_INTERFACE
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout endpoint for users.
    """
    logout(request)
    return Response({'detail': 'Logout successful'})

