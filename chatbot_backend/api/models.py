from django.db import models
from django.conf import settings

# PUBLIC_INTERFACE
class ChatMessage(models.Model):
    """
    Represents a message in a chat session.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_messages'
    )
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message[:30]}..."

