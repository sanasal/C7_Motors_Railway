from django import forms
from . import models 
from . models import customers_data

class Customers_Data(forms.ModelForm):
    class Meta:
        model = customers_data
        fields = ['cars', 'name', 'email', 'mobile_phone', 'pick_up_location', 'pick_up_date' , 'pick_up_time']