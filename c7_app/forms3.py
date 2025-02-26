from django import forms
from . import models 
from . models import InstallmentsCustomerWithoutDP

class Installments_Customers_Data(forms.ModelForm):
    class Meta:
        model = InstallmentsCustomerWithoutDP
        fields =['cars', 'name', 'email', 'mobile_phone',
                 'passport', 'driver_license' , 'personal_identification_card',
                 'salary_certificate','bank_statement' ,
                 'pick_up_location', 'pick_up_date' , 'pick_up_time']