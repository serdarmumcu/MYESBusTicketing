from django import forms
from busticket.models import City,Bus,Driver,Trip
from datetimewidget.widgets import DateTimeWidget,DateWidget
from datetime import timedelta,datetime


class BusForm(forms.ModelForm):  
    class Meta:  
        model = Bus  
        fields = ['plate_text', 'brand_name', 'status','seat_count','bus_company']
        widgets = { 'plate_text': forms.TextInput(attrs={ 'class': 'form-control' }), 
            'brand_name': forms.TextInput(attrs={ 'class': 'form-control' }),
            'status': forms.CheckboxInput(attrs={ 'class': 'form-control' }),
            'seat_count': forms.NumberInput(attrs={ 'class': 'form-control' }),
            'bus_company': forms.HiddenInput(attrs={ 'class': 'form-control' }),
      }

class DriverForm(forms.ModelForm):  
    class Meta:  
        model = Driver  
        fields = ['name', 'date_of_birth', 'years_of_experience']
        now = datetime.now()
        years = 18
        days_per_year = 365.24
        years_removed = timedelta(days = (years*days_per_year))
        now = now - years_removed
        widgets = { 'name': forms.TextInput(attrs={ 'class': 'form-control' }), 
            'date_of_birth': DateWidget(attrs={'id':"date_of_birth_id"}, usel10n = True, bootstrap_version=3, options = {'endDate': now.strftime("%Y-%m-%d %H:%M:%S")}), 
            'years_of_experience': forms.NumberInput(attrs={ 'class': 'form-control' }),
      }

class TripForm(forms.ModelForm):
    class Meta:  
        model = Trip  
        fields = ['trip_no','bus', 'driver', 'from_city', 'to_city', 'trip_date','price']
        now = datetime.now()
        hours_added = timedelta(hours = 3)
        now = now + hours_added
        widgets = { 
            'trip_no': forms.TextInput(attrs={'class': 'form-control' ,'readonly': 'readonly'}), 
            'bus': forms.Select(attrs={ 'class': 'form-control' }), 
            'driver': forms.Select(attrs={ 'class': 'form-control' }), 
            'from_city': forms.Select(attrs={ 'class': 'form-control' }), 
            'to_city': forms.Select(attrs={ 'class': 'form-control' }), 
            'trip_date': DateTimeWidget(attrs={'id':"trip_date_id"}, usel10n = True, bootstrap_version=3, options = {'startDate': now.strftime("%Y-%m-%d %H:%M:%S")}), 
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }     
    
    def clean(self):
        cleaned_data = super().clean()
        first_city = cleaned_data.get('from_city')
        second_city = cleaned_data.get('to_city')

        if first_city == second_city:
            raise forms.ValidationError('From city and To city selections cannot be the same')


    def __init__(self,buscompany, *args, **kwargs):
        super(TripForm, self).__init__(*args, **kwargs)
        self.fields["bus"].queryset = Bus.objects.filter(bus_company=buscompany,status=True)
        self.fields["driver"].queryset = Driver.objects.filter(bus_company=buscompany)

# class CreateNewBus(forms.Form):
#     plate_text = forms.CharField(label="Plate", max_length=30)
#     brand_name = forms.CharField(label="Brand", max_length=30)
#     status = forms.BooleanField(label="Is Active")