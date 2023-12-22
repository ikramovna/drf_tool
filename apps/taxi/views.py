from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.taxi.models import Seat, Driver, Booking
from apps.taxi.serializers import DriverModelSerializer, SeatModelSerializer, BookingSerializer, DriverSerializer


class CarSearchAPIView(ListAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    filter_backends = [SearchFilter]
    search_fields = ['from_place', 'to_place', 'date']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('from_place', openapi.IN_QUERY, description='Starting location',
                              type=openapi.TYPE_STRING),
            openapi.Parameter('to_place', openapi.IN_QUERY, description='Destination location',
                              type=openapi.TYPE_STRING),
            openapi.Parameter('date', openapi.IN_QUERY, description='Date',
                              type=openapi.TYPE_STRING),
        ],
        operation_description='Search for cars based on starting and destination locations.'
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class MyBookingsAPIView(ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


class SeatCreateAPIView(ListCreateAPIView):
    queryset = Seat.objects.all()
    serializer_class = SeatModelSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DriverCreateAPIView(CreateAPIView):
    serializer_class = DriverModelSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response_data = serializer.data
        return Response(response_data)


class DriverDetailAPIView(UpdateAPIView, DestroyAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverModelSerializer


class BookingCreateAPIView(CreateAPIView):
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
