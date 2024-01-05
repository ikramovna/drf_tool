from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import SearchFilter
from rest_framework.generics import UpdateAPIView, DestroyAPIView, ListCreateAPIView, ListAPIView, CreateAPIView

from .pagination import CustomPagination
from .serializers import SeatModelSerializer, DriverModelSerializer, BookingSerializer
from ..taxi.models import Driver, Seat, Booking


# Search

class CarSearchAPIView(ListAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverModelSerializer
    filter_backends = [SearchFilter]
    search_fields = ['from_place', 'to_place']
    pagination_class = CustomPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('from_place', openapi.IN_QUERY, description='Starting location',
                              type=openapi.TYPE_STRING),
            openapi.Parameter('to_place', openapi.IN_QUERY, description='Destination location',
                              type=openapi.TYPE_STRING),
        ],
        operation_description='Search for cars based on starting and destination locations.'
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# Seat List
class SeatCreateAPIView(ListAPIView):
    queryset = Seat.objects.all()
    serializer_class = SeatModelSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DriverCreateAPIView(ListCreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverModelSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


#  Driver Update and Delete
class DriverDetailAPIView(UpdateAPIView, DestroyAPIView):
    """
    {
      "first_name": "Ali",
      "last_name": "Aliyev",
      "phone": "123456789",
      "account_tg": "aliyevvvv03",
      "model": "Malibu",
      "from_place": "Tashkent",
      "to_place": "Bukhara",
      "date": "2023-12-31",
      "price": "1000",
      "seat": [
        {
          "seat": 1,
          "is_booked": true
        },
        {
          "seat": 2,
          "is_booked": false
        }
      ]
    }
    """

    queryset = Driver.objects.all()
    serializer_class = DriverModelSerializer


# Booking Post

class BookingCreateAPIView(CreateAPIView):
    """
           {
      "first_name": "Ali",
      "last_name": "Aliyev",
      "seat": [
        {"id": 1, "is_booked": true, "seat": 2},
        {"id": 3, "is_booked": true, "seat": 4}
      ]
    }
    """
    serializer_class = BookingSerializer


class MyBookingsAPIView(ListAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


class BookingDetailAPIView(UpdateAPIView, DestroyAPIView):
    """
           {
      "first_name": "Ali",
      "last_name": "Aliyev",
      "seat": [
        {"id": 1, "is_booked": true, "seat": 2},
        {"id": 3, "is_booked": true, "seat": 4}
      ]
    }
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
