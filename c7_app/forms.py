from django import forms
from . models import customers_data  , InstallmentsCustomer , InstallmentsCustomerWithoutDP 
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm 
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username' , 'email' , 'password1' , 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap-style classes
        for field in self.fields.values():
            field.widget.attrs.update({
                'class' : 'form-control', 
                'style': 'margin-bottom: 15px;',
            })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists.")
        return email
    
class Customers_Data(forms.ModelForm):
    class Meta:
        model = customers_data
        fields = ['cars', 'name', 'email', 'mobile_phone', 'pick_up_location', 'pick_up_date' , 'pick_up_time']

class Installments_Customers_Data(forms.ModelForm):
    class Meta:
        model = InstallmentsCustomer
        fields =['cars', 'name', 'email', 'mobile_phone',
                 'passport', 'driver_license' , 'personal_identification_card',
                 'salary_certificate','bank_statement' ,
                 'pick_up_location', 'pick_up_date' , 'pick_up_time']

class Installments_Customers_Data_Without_DP(forms.ModelForm):
    class Meta:
        model = InstallmentsCustomerWithoutDP
        fields =['cars', 'name', 'email', 'mobile_phone',
                 'passport', 'driver_license' , 'personal_identification_card',
                 'salary_certificate','bank_statement' ,
                 'pick_up_location', 'pick_up_date' , 'pick_up_time']