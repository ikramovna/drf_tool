from django.urls import path

from apps.taxi.views import DriverCreateAPIView, SeatCreateAPIView, DriverDetailAPIView

urlpatterns = [
    path('car', SeatCreateAPIView.as_view()),
    path('driver', DriverCreateAPIView.as_view()),
    path('drivers/<int:pk>/', DriverDetailAPIView.as_view()),
]
