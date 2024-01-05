from django.urls import path

from apps.taxii.views import DriverCreateAPIView, DriverDetailAPIView, SeatCreateAPIView, CarSearchAPIView, \
    BookingCreateAPIView, MyBookingsAPIView, BookingDetailAPIView

urlpatterns = [
    path('seat', SeatCreateAPIView.as_view()),
    path('driver', DriverCreateAPIView.as_view()),
    path('booking', BookingCreateAPIView.as_view()),
    path('booking/my', MyBookingsAPIView.as_view()),
    path('driver/<int:pk>/', DriverDetailAPIView.as_view()),
    path('booking/<int:pk>/', BookingDetailAPIView.as_view()),
    path('search', CarSearchAPIView.as_view()),

]
