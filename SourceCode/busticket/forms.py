from django import forms
from busticket.models import City,Bus,Driver,Trip
from datetimewidget.widgets import DateTimeWidget

class BusForm(forms.ModelForm):  
    class Meta:  
        model = Bus  
        fields = ['plate_text', 'brand_name', 'status']
        widgets = { 'plate_text': forms.TextInput(attrs={ 'class': 'form-control' }), 
            'brand_name': forms.TextInput(attrs={ 'class': 'form-control' }),
            'status': forms.CheckboxInput(attrs={ 'class': 'form-control' }),
      }

class DriverForm(forms.ModelForm):  
    class Meta:  
        model = Driver  
        fields = ['name', 'date_of_birth', 'years_of_experience']
        widgets = { 'name': forms.TextInput(attrs={ 'class': 'form-control' }), 
            'date_of_birth': forms.NumberInput(attrs={ 'type': 'date' }),
            'years_of_experience': forms.NumberInput(attrs={ 'class': 'form-control' }),
      }

class TripForm(forms.ModelForm):
    class Meta:  
        model = Trip  
        fields = ['trip_no','bus', 'driver', 'from_city', 'to_city', 'trip_date']
        widgets = { 
            'trip_no': forms.TextInput(attrs={'class': 'form-control' ,'readonly': 'readonly'}), 
            'bus': forms.Select(attrs={ 'class': 'form-control' }), 
            'driver': forms.Select(attrs={ 'class': 'form-control' }), 
            'from_city': forms.Select(attrs={ 'class': 'form-control' }), 
            'to_city': forms.Select(attrs={ 'class': 'form-control' }), 
            'trip_date': DateTimeWidget(attrs={'id':"yourdatetimeid"}, usel10n = True, bootstrap_version=3), 
        }     

# class CreateNewBus(forms.Form):
#     plate_text = forms.CharField(label="Plate", max_length=30)
#     brand_name = forms.CharField(label="Brand", max_length=30)
#     status = forms.BooleanField(label="Is Active")