from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CarForm(forms.ModelForm):

    technical_features = forms.ModelMultipleChoiceField(
        queryset=TechnicalFeature.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    
    driver_assistance_and_safty = forms.ModelMultipleChoiceField(
        queryset=DriverAssistanceAndSafty.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    
    comfort_and_convenience = forms.ModelMultipleChoiceField(
        queryset=ComfortAndConvenience.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    
    exterior = forms.ModelMultipleChoiceField(
        queryset=Exterior.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comfort_and_convenience'].queryset = ComfortAndConvenience.objects.all()
        self.fields['technical_features'].queryset = TechnicalFeature.objects.all()
        self.fields['driver_assistance_and_safty'].queryset = DriverAssistanceAndSafty.objects.all()
        self.fields['exterior'].queryset = Exterior.objects.all()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    age = forms.IntegerField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'age', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
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
        fields = ['car', 'name', 'mobile_phone', 'language', 'payment_method']
