from django.contrib import admin
from busticket.models import Bus,Trip,Driver,City
# Register your models here.

admin.site.register(City)
admin.site.register(Bus)
admin.site.register(Driver)
admin.site.register(Trip)