from django.contrib import admin
from busticket.models import Bus,Trip,Driver,City,BusCompany
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
# Register your models here.

class BusCompanyInline(admin.StackedInline):
    model = BusCompany
    can_delete = False
    verbose_name_plural = 'buscompanies'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (BusCompanyInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(City)
admin.site.register(Bus)
admin.site.register(Driver)
admin.site.register(Trip)
admin.site.register(BusCompany)