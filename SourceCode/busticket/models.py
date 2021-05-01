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
    trip_no = models.UUIDField(default=uuid4)
    bus = models.ForeignKey(Bus, on_delete=models.PROTECT)
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT,blank=True,null=True)
    from_city = models.ForeignKey(City, related_name='f_city', on_delete=models.CASCADE,blank=True,null=True)
    to_city = models.ForeignKey(City, related_name='t_city', on_delete=models.CASCADE,blank=True,null=True)
    trip_date = models.DateTimeField(blank=True)
    bus_company = models.ForeignKey(BusCompany, on_delete=models.CASCADE, editable=False,blank=True,null=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['bus', 'from_city','to_city','trip_date'], name='unique trip')
        ]