from django import forms
from django.contrib.auth.models import User
from user.models import *
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import Kyc, Kyc_member, Kyc_primary_police, Kyc_secondary_police

primary_document = (
    ('Foreign Passport (current)', 'Foreign Passport (current)'),
    ('Australian Passport (current or expired within last 2 years but not cancelled)',
     'Australian Passport (current or expired within last 2 years but not cancelled)'),
    ('Australian Citizenship Certificate', 'Australian Citizenship Certificate'),
    (
        'Full Birth certificate (not birth certificate extract)',
        'Full Birth certificate (not birth certificate extract)'),
    (
        'Certificate of Identity issued by the Australian Government to refugees and non Australian citizens for entry to Australia',
        'Certificate of Identity issued by the Australian Government to refugees and non Australian citizens for entry to Australia'),
    ('Australian Driver Licence/Learner’s Permit', 'Australian Driver Licence/Learner’s Permit'),
    ('Current (Australian) Tertiary Student Identification Card',
     'Current (Australian) Tertiary Student Identification Card'),
    ('Photo identification card issued for Australian regulatory purposes (e.g. Aviation/Maritime Security '
     'identification, security industry etc.)',
     'Photo identification card issued for Australian regulatory purposes (e.g. Aviation/Maritime Security identification, security industry etc.)'),
    ('Government employee ID (Australian Federal/State/Territory)',
     'Government employee ID (Australian Federal/State/Territory)'),
    ('Defence Force Identity Card (with photo or signature)',
     'Defence Force Identity Card (with photo or signature)'),

)
secondary_document = (
    ('Department of Veterans Affairs (DVA) card', 'Department of Veterans Affairs (DVA) card'),
    ('Centrelink card (with reference number)',
     'Centrelink card (with reference number)'),
    ('Birth Certificate Extract', 'Birth Certificate Extract'),
    (
        'Birth card (NSW Births, Deaths, Marriages issue only)',
        'Birth card (NSW Births, Deaths, Marriages issue only)'),
    (
        'Medicare card',
        'Medicare card'),
    ('Credit card or account card', 'Credit card or account card'),
    ('Australian Marriage certificate (Australian Registry issue only)',
     'Australian Marriage certificate (Australian Registry issue only)'),
    ('Decree Nisi / Decree Absolute (Australian Registry issue only)',
     'Decree Nisi / Decree Absolute (Australian Registry issue only)'),
    ('Change of name certificate (Australian Registry issue only)',
     'Change of name certificate (Australian Registry issue only)'),
    ('Bank statement (showing transactions)',
     'Bank statement (showing transactions)'),
    ('Property lease agreement - current address', 'Property lease agreement - current address'),
    ('Taxation assessment notice',
     'Taxation assessment notice'),
    ('Australian Mortgage Documents - Current address', 'Australian Mortgage Documents - Current address'),
    (
        'Rating Authority - Current address eg Land Rates',
        'Rating Authority - Current address eg Land Rates'),
    (
        'Utility Bill - electricity, gas, telephone - Current address (less than 12 months old)',
        'Utility Bill - electricity, gas, telephone - Current address (less than 12 months old)'),
    ('Reference from Indigenous Organisation', 'Reference from Indigenous Organisation'),
    ('Documents issued outside Australia (equivalent to Australian documents).Must have official translation attached',
     'Documents issued outside Australia (equivalent to Australian documents).Must have official translation attached'),

)


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
    name = forms.CharField(max_length=30, label='Name',
                           widget=forms.TextInput(attrs={'id': 'name_value', 'readonly': True}))
    agentId = forms.CharField(max_length=30, label='Agent ID')
    email = forms.EmailField(max_length=300, label='Email Id', widget=forms.EmailInput(attrs={'id': 'email_value', 'readonly': True}))
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Please enter valid phone number. Correct format is 04XXXXXXXX")
    phone = forms.CharField(validators=[phone_regex], max_length=18, label="Phone Number", required=True,
                            widget=forms.TextInput(attrs={'id': 'phone_value', 'readonly': True}))
    residential_Address = forms.CharField(label="Residential Address", widget=forms.Textarea())
    communication_address = forms.CharField(label="Communication Address", widget=forms.Textarea())

    class Meta:
        model = Kyc
        fields = [
            'name',
            'agentId',
            'email',
            'phone',
            'residential_Address',
            'communication_address'
        ]


class KycFormprimary(forms.ModelForm):
    name_of_document = forms.ChoiceField(label="Select the document", choices=primary_document)
    document = forms.FileField(label="Document")

    class Meta:
        model = Kyc_primary_police
        fields = [
            'name_of_document',
            'document'
        ]


class KycFormsecondary(forms.ModelForm):
    name_of_Sdocument = forms.ChoiceField(label="Select the document for Police Verification",
                                          choices=secondary_document)
    Sdocument = forms.FileField(label="Police verification Document")

    class Meta:
        model = Kyc_secondary_police
        fields = [
            'name_of_Sdocument',
            'Sdocument'
        ]


class KycMemberForm(forms.ModelForm):
    afca_membership = forms.CharField(label="AFCA Membership")
    Aggregator_contractor = forms.CharField(label='Aggregator Contractor')
    Aggregator_ManagerName = forms.CharField(label="Aggregator Manager Name")
    Aggregator_ManagerNumber = forms.CharField(label="Aggregator Manger Number")
    ABN_Number = forms.CharField(label="ABN Number")
    Diploma_certificate = forms.FileField(label="Diploma certificate")

    class Meta:
        model = Kyc_member
        fields = [
            'afca_membership',
            'Aggregator_contractor',
            'Aggregator_ManagerName',
            'Aggregator_ManagerNumber',
            'ABN_Number',
            'Diploma_certificate'
        ]
