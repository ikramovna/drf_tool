from django.urls import path

from apps.taxi.views import SeatCreateAPIView, CreateDriverWithSeatAPIView

urlpatterns = [
    path('car', SeatCreateAPIView.as_view()),
    path('driver', CreateDriverWithSeatAPIView.as_view()),


]
