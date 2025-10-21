from django.urls import path
from .views import predict_emotion_view
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='dashboard.html'), name='home'),
    path('predict_emotion/', predict_emotion_view, name='predict_emotion'),
]
