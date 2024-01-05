from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.taxi.models import *


# Seat Serializer
class SeatModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = "__all__"


# Driver Post Serializer
class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverSeat
        fields = ('seat', 'is_booked')


class DriverModelSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    seat = SeatSerializer(many=True, write_only=True)

    class Meta:
        model = Driver
        fields = (
            'id', 'first_name',
            'last_name', 'phone',
            'account_tg', 'model',
            'from_place', 'to_place',
            'date', 'price', 'user', "seats", "seat")

    def validate_seat(self, seat_data):
        if not seat_data:
            raise serializers.ValidationError("At least one seat must be provided.")
        return seat_data

    def validate(self, data):
        date = data.get('date')
        if date and date < timezone.now().date():
            raise serializers.ValidationError("Date must be today or later")
        from_place = data.get('from_place')
        to_place = data.get('to_place')
        if from_place and to_place and from_place == to_place:
            raise serializers.ValidationError("From place and to place must be different.")
        return data

    def create(self, validated_data):
        seat_data = validated_data.pop('seat')
        driver = Driver.objects.create(**validated_data)
        for seat in seat_data:
            DriverSeat.objects.create(driver=driver, seat=seat['seat'], is_booked=seat['is_booked'])
        return driver


class BookingSerializer(serializers.ModelSerializer):
    seat = serializers.JSONField()

    class Meta:
        model = Booking
        fields = ['id','first_name', 'last_name', 'seat', 'total_price']
        read_only_fields = ['total_price']

    def seat_info(self, seat_info, user):
        seat_id, is_booked = seat_info.get('id'), seat_info.get('is_booked', False)
        try:
            driver_seat = DriverSeat.objects.get(id=seat_id)
            if is_booked and driver_seat.is_booked and driver_seat.driver != user:
                raise ValidationError("This seat is already booked by another user.")
            driver_seat.is_booked = is_booked
            driver_seat.save()
            return driver_seat.driver.price if hasattr(driver_seat.driver, 'price') and is_booked else 0
        except DriverSeat.DoesNotExist:
            return 0

    def create(self, validated_data):
        user = self.context['request'].user
        seat_data = validated_data.pop('seat', [])
        total_price = sum(self.seat_info(seat_info, user) for seat_info in seat_data)
        return Booking.objects.create(user=user, seat=seat_data, total_price=total_price, **validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        seat_data = validated_data.get('seat', instance.seat)
        total_price = sum(self.seat_info(seat_info, user) for seat_info in seat_data)

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.seat = seat_data
        instance.total_price = total_price
        instance.save()

        return instance
