from django.urls import path

from .views import PaymentAPIView, AddCardAPIView


urlpatterns = [
    path('', PaymentAPIView.as_view()),
    path('<int:id>/', PaymentAPIView.as_view()),
    path('card/add/', AddCardAPIView.as_view()),
]
