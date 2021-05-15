from django import forms
from busticket.models import City,Bus,Driver,Trip,Reservation
from datetimewidget.widgets import DateTimeWidget,DateWidget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
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
        fields = ['id','bus', 'driver', 'from_city', 'to_city', 'trip_date','price']
        now = datetime.now()
        hours_added = timedelta(hours = 3)
        now = now + hours_added
        widgets = { 
            'id': forms.TextInput(attrs={'class': 'form-control' ,'readonly': 'readonly'}), 
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

class ReservationForm(forms.ModelForm):
    class Meta:  
        model = Reservation  
        fields = ['trip', 'seat_no','reservation_date','passenger']
        widgets = { 
            'trip': forms.HiddenInput(attrs={ 'class': 'form-control' }), 
            'seat_no': forms.NumberInput(attrs={'class': 'form-control'}),
            'reservation_date': forms.HiddenInput(attrs={ 'class': 'form-control' }),
            'passenger': forms.HiddenInput(attrs={ 'class': 'form-control' }),
        }     

    def clean(self):
        cleaned_data = super().clean()
        passenger = cleaned_data.get('passenger')
        reservationCount = Reservation.objects.filter(passenger=passenger,is_ticket=False).count()

        if self.is_insert and reservationCount == 5:
             raise forms.ValidationError('It is not allowed to make more than 5 reservation')

    def __init__(self,trip,passenger,is_insert=False, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.is_insert = is_insert
        self.fields["trip"].initial = trip
        self.fields["passenger"].initial = passenger

        

class SearchForm(forms.ModelForm):
    DATE_CHOICES= [
    ('', 'All'),
    ('Today', 'Today'),
    ('This Week', 'This Week'),
    ('This Month', 'This Month'),
    ('This Year', 'This Year'),
    ]
    date_choice= forms.CharField(label='When do you want to travel?', required=False, widget=forms.Select(choices=DATE_CHOICES,attrs={ 'class': 'form-control' }))
    
    class Meta:  
        model = Trip  
        fields = ['from_city', 'to_city','bus_company']
        widgets = { 
            'from_city': forms.Select(attrs={ 'class': 'form-control' }), 
            'to_city': forms.Select(attrs={ 'class': 'form-control' }), 
            'bus_company': forms.Select(attrs={ 'class': 'form-control' }), 
        }     

class RegisterForm(UserCreationForm):
    name = forms.CharField(max_length=30,required=True)
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
