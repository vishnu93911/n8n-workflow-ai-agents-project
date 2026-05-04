# core/urls.py or dashboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # Loads the HTML page
    path('chat/', views.chat_with_agent, name='chat_with_agent'), # The JS calls this
]