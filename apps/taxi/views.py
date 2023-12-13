from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.response import Response

from apps.taxi.models import Seat
from apps.taxi.serializers import SeatModelSerializer, DriverSeatSerializer


class SeatCreateAPIView(ListCreateAPIView):
    queryset = Seat.objects.all()
    serializer_class = SeatModelSerializer

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class CreateDriverWithSeatAPIView(CreateAPIView):
    serializer_class = DriverSeatSerializer

    def create(self, request, *args, **kwargs):
        driver_data = request.data.get('driver', {})
        seat_data = request.data.get('seat', {})

        driver_serializer = DriverSeatSerializer(data=driver_data)
        driver_serializer.is_valid(raise_exception=True)

        seat_serializer = SeatModelSerializer(data=seat_data)
        seat_serializer.is_valid(raise_exception=True)

        driver_instance = driver_serializer.save(user=request.user)

        seat_instance = seat_serializer.save()

        driver_seat_data = {
            'driver': driver_instance.id,
            'seat': seat_instance.id,
            'is_booked': False,
        }

        driver_seat_serializer = DriverSeatSerializer(data=driver_seat_data)
        driver_seat_serializer.is_valid(raise_exception=True)
        driver_seat_serializer.save()

        response_data = {
            "driver": driver_serializer.data,
            "seat": seat_serializer.data,
            "is_booked": False
        }

        return Response(response_data)
