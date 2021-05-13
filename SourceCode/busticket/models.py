from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User

# Create your models here.

class BusCompany(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30,unique=True,default='Default Bus Company')
    def __str__(self):
        return self.name

class Bus(models.Model):
    plate_text = models.CharField(max_length=30,unique=True)
    brand_name = models.CharField(max_length=30,default='Mercedes Benz')
    status = models.BooleanField(default=True)
    seat_count = models.IntegerField(default=52)
    bus_company = models.ForeignKey(BusCompany, on_delete=models.CASCADE, blank=True,null=True)
    def __str__(self):
        return self.plate_text

class Driver(models.Model):
    name = models.CharField(max_length=30,default='Unknown Driver',unique=True)
    date_of_birth = models.DateField()
    years_of_experience = models.IntegerField()
    bus_company = models.ForeignKey(BusCompany, on_delete=models.CASCADE, editable=False,blank=True,null=True)
    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=30,unique=True)
    def __str__(self):
        return self.name

class Trip(models.Model):
    trip_no = models.UUIDField(default=uuid4,max_length=8)
    bus = models.ForeignKey(Bus, on_delete=models.PROTECT)
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT,blank=True,null=True)
    from_city = models.ForeignKey(City, related_name='f_city', on_delete=models.CASCADE,blank=True,null=True)
    to_city = models.ForeignKey(City, related_name='t_city', on_delete=models.CASCADE,blank=True,null=True)
    trip_date = models.DateTimeField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    bus_company = models.ForeignKey(BusCompany, on_delete=models.CASCADE, editable=True,blank=True,null=True)
    def __str__(self):
        return str(self.trip_no)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['bus', 'from_city','to_city'], name='unique trip')
        ]

class Passenger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30,unique=True,default='Default Passenger')
    def __str__(self):
        return self.name

class Reservation(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.PROTECT,blank=True,null=True)
    seat_no = models.IntegerField(default=1)
    reservation_date = models.DateTimeField(blank=True)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, editable=True,blank=True,null=True)
    is_ticket = models.BooleanField(default=False)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['trip', 'seat_no'], name='unique seat')
        ]