from django.urls import path

from apps.taxi.views import DriverCreateAPIView, SeatCreateAPIView, DriverDetailAPIView, BookingCreateAPIView, \
    CarSearchAPIView, MyBookingsAPIView

urlpatterns = [
    # path('car', SeatCreateAPIView.as_view()),
    # path('driverrr', DriverCreateAPIView.as_view()),
    # path('booking', BookingCreateAPIView.as_view()),
    # path('booking/my', MyBookingsAPIView.as_view()),
    # path('search', CarSearchAPIView.as_view()),
    # path('driver/<int:pk>/', DriverDetailAPIView.as_view()),

]