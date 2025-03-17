from django.urls import path
from .views import send_location_sms, make_emergency_call, chat_with_ai, predict_safety_rating

urlpatterns = [
    path('sms', send_location_sms, name='send_sms'),
    path('call', make_emergency_call, name='make_call'),
    path('ai/prompt', chat_with_ai, name='chat_with_ai'),  # AI chat route
    path('ai/predict', predict_safety_rating, name='predict')
]
