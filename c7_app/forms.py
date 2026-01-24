from django import forms
from . models import *
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm 
from django.contrib.auth.models import User 

class CarForm(forms.ModelForm):
    extra_features = forms.ModelMultipleChoiceField(
        queryset=ExtraFeature.objects.all(),
        required=False,
        widget=forms.TypedMultipleChoiceField
    )

    technical_features = forms.ModelMultipleChoiceField(
        queryset=TechnicalFeature.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Car
        fields = '__all__'


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    age = forms.IntegerField(required=True)
    class Meta:
        model = User
        fields = ('username' , 'email' , 'age' , 'password1' , 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

class RequestsForm(forms.ModelForm):
    class Meta:
        model = RequestsData
        fields = [ 'car' ,'name', 'mobile_phone' , 'language' , 'payment_method']