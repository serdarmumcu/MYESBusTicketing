from django.db import models
from uuid import uuid4

# Create your models here.
class Bus(models.Model):
    plate_text = models.CharField(max_length=30,unique=True)
    brand_name = models.CharField(max_length=30,default='Mercedes Benz')
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.plate_text
    class Meta:  
        db_table = "busticket_bus"


class Driver(models.Model):
    name = models.CharField(max_length=30,default='Unknown Driver')
    date_of_birth = models.DateField()
    years_of_experience = models.IntegerField()
    def __str__(self):
        return self.name
    class Meta:  
        db_table = "busticket_driver"

class City(models.Model):
    name = models.CharField(max_length=30,unique=True)

    def __str__(self):
        return self.name

class Trip(models.Model):
    trip_no = models.UUIDField(default=uuid4)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE,blank=True,null=True)
    from_city = models.ForeignKey(City, related_name='f_city', on_delete=models.CASCADE,blank=True,null=True)
    to_city = models.ForeignKey(City, related_name='t_city', on_delete=models.CASCADE,blank=True,null=True)
    trip_date = models.DateTimeField(blank=True)

    class Meta:  
        db_table = "busticket_trip"