from django.urls import path

from .views import ProductsAPIView


urlpatterns = [
    path('', ProductsAPIView.as_view()),
    path('<int:id>/', ProductsAPIView.as_view())
]
