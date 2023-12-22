from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.postgres.fields import ArrayField
from django.db.models import *

from apps.shared.drf.models import BaseModel


class Seat(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Driver(Model):
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    phone = CharField(max_length=255)
    account_tg = CharField(max_length=255)
    model = CharField(max_length=255)
    from_place = CharField(max_length=255)
    to_place = CharField(max_length=255)
    date = DateField()
    price = DecimalField(max_digits=10, decimal_places=2)
    user = ForeignKey('auth.User', on_delete=CASCADE, related_name='driver')

    @property
    def seats(self):
        return self.setdriver_set.all().values()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class DriverSeat(Model):
    driver = ForeignKey(Driver, on_delete=CASCADE, related_name='setdriver_set')
    seat = ForeignKey(Seat, on_delete=CASCADE, related_name='driverseat_set')
    is_booked = BooleanField(default=False)

    def __str__(self):
        return f"{self.driver} - {self.seat}"


class Booking(Model):
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    seat = ArrayField(JSONField())
    phone = CharField(max_length=255)
    user = ForeignKey('auth.User', on_delete=CASCADE)
    total_price = DecimalField(max_digits=10, decimal_places=2)
