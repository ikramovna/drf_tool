from rest_framework.serializers import ModelSerializer

from apps.taxi.models import Seat, DriverSeat


class SeatModelSerializer(ModelSerializer):
    class Meta:
        model = Seat
        fields = "__all__"


class DriverSeatSerializer(ModelSerializer):
    seat = SeatModelSerializer()

    class Meta:
        model = DriverSeat
        fields = '__all__'
