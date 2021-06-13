from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator


# Create your models here.

class BusCompany(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30,unique=True,default='Default Bus Company')
    tel_no = models.CharField(max_length=30,default='', blank=True,null=True)
    address = models.CharField(max_length=300,default='', blank=True,null=True)
    email = models.EmailField(max_length=254,default='', blank=True,null=True)
    url = models.URLField(max_length=200,default='', blank=True,null=True)
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
    bus = models.ForeignKey(Bus, on_delete=models.PROTECT)
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT,blank=True,null=True)
    from_city = models.ForeignKey(City, related_name='f_city', on_delete=models.CASCADE,blank=True,null=True)
    to_city = models.ForeignKey(City, related_name='t_city', on_delete=models.CASCADE,blank=True,null=True)
    trip_date = models.DateTimeField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    bus_company = models.ForeignKey(BusCompany, on_delete=models.CASCADE, editable=True,blank=True,null=True)
    def __str__(self):
        return str(self.from_city) + "-" + str(self.to_city) + "-" + str(self.trip_date)[0:10]
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['bus', 'from_city','to_city'], name='unique trip')
        ]

class Passenger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30,default='Default Passenger')
    def __str__(self):
        return self.name

class Transaction(models.Model):
    transaction_date = models.DateTimeField(blank=True)
    charged_value = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    payment_intent = models.CharField(max_length=50,default='')

class Reservation(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.PROTECT,blank=True,null=True)
    seat_no = models.IntegerField(default=1,validators=[MinValueValidator(1), MaxValueValidator(52)])
    reservation_date = models.DateTimeField(blank=True)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, editable=True,blank=True,null=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, editable=True,blank=True,null=True)
    is_ticket = models.BooleanField(default=False)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['trip', 'seat_no'], name='unique seat')
        ]

