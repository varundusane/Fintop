from django import forms
from django.contrib.auth.models import User
from user.models import *
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import Kyc, Kyc_member, Kyc_primary_police, Kyc_secondary_police


# Sign Up Form
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254)
    # phnumber = forms.CharField(label = "Phone Number",required=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Please enter valid phone number. Correct format is 04XXXXXXXX")
    phnumber = forms.CharField(validators=[phone_regex], max_length=18, label="Phone Number", required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'phnumber',
            'email',
            'password1',
            'password2',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')

        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email


class KYCForm(forms.ModelForm):
    class Meta:
        model = Kyc
        fields = '__all__'


class KycFormprimary(forms.ModelForm):
    class Meta:
        model = Kyc_primary_police
        fields = [
            'name_of_document',
            'document'
        ]


class KycFormsecondary(forms.ModelForm):
    class Meta:
        model = Kyc_secondary_police
        fields = [
            'name_of_Sdocument',
            'Sdocument'
        ]
class KycMemberForm(forms.ModelForm):
    class Meta:
        model = Kyc_member
        fields = [
            'afca_membership',
            'aggreator_contractor',
            'Aggregato_ManagerName',
            'Aggregato_ManagerNumber',
            'ABN_Number',
            'Diploma_certificate'
        ]