from django.urls import path
from .views import health, message, history, login_view, logout_view, register_view

urlpatterns = [
    path('health/', health, name='Health'),
    path('message/', message, name='ChatMessage'),
    path('history/', history, name='ChatHistory'),
    path('login/', login_view, name='Login'),
    path('logout/', logout_view, name='Logout'),
    path('register/', register_view, name='Register')
]
