from django import forms
from busticket.models import Bus  

class BusForm(forms.ModelForm):  
    class Meta:  
        model = Bus  
        fields = ['plate_text', 'brand_name', 'status']
        widgets = { 'plate_text': forms.TextInput(attrs={ 'class': 'form-control' }), 
            'brand_name': forms.TextInput(attrs={ 'class': 'form-control' }),
            'status': forms.CheckboxInput(attrs={ 'class': 'form-control' }),
      }

# class CreateNewBus(forms.Form):
#     plate_text = forms.CharField(label="Plate", max_length=30)
#     brand_name = forms.CharField(label="Brand", max_length=30)
#     status = forms.BooleanField(label="Is Active")