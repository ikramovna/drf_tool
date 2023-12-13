from rest_framework import serializers
from .models import Driver, DriverSeat, Seat
from django.utils import timezone


class SeatModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = "__all__"


class DriverSeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverSeat
        fields = ['is_booked', 'seat']


class DriverModelSerializer(serializers.ModelSerializer):
    seat = DriverSeatSerializer(many=True, write_only=True)

    class Meta:
        model = Driver
        exclude = ('user',)

    def validate_seat(self, seat_data):
        if not seat_data:
            raise serializers.ValidationError("At least one seat must be provided.")
        return seat_data

    def validate(self, data):
        date = data.get('date')
        if date and date < timezone.now().date():
            raise serializers.ValidationError("Date cannot be in the past.")

        from_place = data.get('from_place')
        to_place = data.get('to_place')
        if from_place and to_place and from_place == to_place:
            raise serializers.ValidationError("From place and to place must be different.")

        return data

    def create(self, validated_data):
        seat_data = validated_data.pop('seat')

        user = self.context['request'].user
        driver = Driver.objects.create(user=user, **validated_data)

        for seat_info in seat_data:
            seat_id = seat_info['seat']
            is_booked = seat_info['is_booked']
            seat = Seat.objects.get(id=seat_id.id if isinstance(seat_id, Seat) else seat_id)
            DriverSeat.objects.create(driver=user, seat=seat, is_booked=is_booked)

        return driver
