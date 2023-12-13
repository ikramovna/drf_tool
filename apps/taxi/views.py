from rest_framework.generics import ListCreateAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response

from apps.taxi.models import Seat, Driver
from apps.taxi.serializers import DriverModelSerializer, SeatModelSerializer


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
