from django.utils import timezone
from rest_framework import serializers

from .models import Driver, DriverSeat, Seat, Booking


class SeatModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = "__all__"


class DriverSeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverSeat
        fields = ['seat', 'is_booked']


# ------
class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverSeat
        fields = ['seat', 'is_booked']


class DriverSerializer(serializers.ModelSerializer):
    seat = SeatSerializer(many=True, source='driverseat_set', read_only=True)

    class Meta:
        model = Driver
        fields = ['id', 'first_name', 'last_name', 'phone', 'account_tg', 'model', 'from_place', 'to_place', 'date',
                  'price', 'seat']


# -----
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


class SeatSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    is_booked = serializers.BooleanField()
    seat = serializers.IntegerField()


class BookingSerializer(serializers.ModelSerializer):
    seat = serializers.JSONField()

    class Meta:
        model = Booking
        fields = ['first_name', 'last_name', 'seat', 'total_price']
        read_only_fields = ['total_price']

    def create(self, validated_data):
        user = self.context['request'].user
        seat_data = validated_data.pop('seat', [])

        total_price = 0

        for seat_info in seat_data:
            seat_id = seat_info.get('id')
            is_booked = seat_info.get('is_booked', False)

            try:
                driver_seat = DriverSeat.objects.get(id=seat_id)

                driver_seat.is_booked = is_booked
                driver_seat.save()

                driver = driver_seat.driver

                if hasattr(driver, 'price') and is_booked:
                    print(f"Driver {driver.id} Price: {driver.price}")

                    total_price += driver.price

            except DriverSeat.DoesNotExist:
                pass

        print(f"Total Price: {total_price}")

        booking = Booking.objects.create(user=user, seat=seat_data, total_price=total_price, **validated_data)
        return booking
