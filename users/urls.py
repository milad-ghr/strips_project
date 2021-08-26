from django.urls import path

from .views import UserAPIView


urlpatterns = [
    path('', UserAPIView.as_view()),
    path('<int:id>/', UserAPIView.as_view())
]
