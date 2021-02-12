from django import forms
from django.contrib.auth.models import User
from user.models import *
from django.contrib.auth.forms import UserCreationForm

# Sign Up Form


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254)
    phnumber = forms.CharField(label="Phone Number", required=False)

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

# Profile Form


class ProfileForm(forms.ModelForm):
    username = forms.CharField(disabled=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]
        help_texts = {
            'username': None,
        }


class ProfileForms(forms.ModelForm):
    phnumber = forms.Field(label="Phone Number")

    class Meta:
        model = Profile
        fields = ['phnumber']


class ReferralForm(forms.ModelForm):
    user = forms.Field(label="Lead Name")

    class Meta:
        model = Referral
        fields = [
            'user',
            'status',
            'commissions'
        ]


class BankInfoForm(forms.ModelForm):
    bankname = forms.CharField(label="Bank Name", max_length=50)
    acname = forms.CharField(label="Account Name", max_length=50)
    acno = forms.CharField(label="Account Number")
    bankisc = forms.CharField(label="BSB", max_length=50)

    class Meta:
        model = BankInfo
        fields = [
            'bankname',
            'acname',
            'acno',
            'bankisc',
        ]


class BusinessForm(forms.ModelForm):
    fullname = forms.CharField(label="Full Name", max_length=50)
    signature = forms.CharField(label="Signature Text", max_length=50)

    class Meta:
        model = Business
        fields = [
            'fullname',
            'signature',
        ]


class VerificationForm(forms.ModelForm):
    class Meta:
        model = Verification
        fields = [
            'user',
            'is_bizpartner',
        ]


class LoanForm(forms.ModelForm):
    yesorno = (('---------', '---------'), ("Yes", "Yes"), ("No", "No"))
    liability_loan = forms.ChoiceField(
        label="Do you have any other additional liabilities ?", choices=yesorno)
    carloan_pay = forms.ChoiceField(
        label="If required, can you pay off the car loan immediately?", choices=yesorno)
    ltype = (("Buy a Home", "Buy a Home"), ("Refinance", "Refinance"))

    class Meta:
        model = Loan
        fields = [
            'loan_type',
            'vehicle',
            'vehicle_worth',
            'vehicle_money',
            'carloan_pay',
            'accounts',
            'superannuation',
            'additional_asset',
            'home_content',
            'credit_card',
            'credit_limit',
            'liability_loan',
            'loans',
            'employment_type',
            'annual_salary',
            'monthly_expense'
        ]
        labels = {
            'loan_type': "Do you want to buy a new house or refinance existing loan ?",
            "vehicle": "Do you have car or any other type of vehicle ?",
            "carloan_pay": "If required, can you apy off car loan immediately ?",
            "accounts": "$ in Saving Accounts ?",
            "superannuation": "$ in Superannuation",
            "additional_asset": "Do you have any additional assets ?",
            "home_content": "Approximate value  of total home contains you may have ?",
            "credit_card": "Do you have any Credit Card ?",
            # "liability_loan": "Do you have any other additional liabilities ?"
        }


class AdditionalAssetsForm(forms.ModelForm):

    description = forms.CharField(
        max_length=15, label="Description", required=False)
    total_value = forms.CharField(label="Total Value", required=False)
    select_assets = (("Term Deposit", "Term Deposit"), ("Shares", "Shares"),
                     ("Managed Funds", "Managed Funds"), ("Gifts", "Gifts"))

    class Meta:
        model = Additional_assets
        fields = [
            'types',
            'description',
            'total_value'
        ]


class AdditionalLiabilitiesForm(forms.ModelForm):
    liability_types = (("tax debt", "tax debt"),
                       ("other lines of credit", "other lines of credit"))
    owned = forms.CharField(required=False)
    description = forms.CharField(
        max_length=15, label="Description", required=False)

    class Meta:
        model = Additional_liabilities
        fields = [
            'types',
            'owned',
            'description'
        ]


class ContactForm(forms.ModelForm):
    name = forms.CharField(label='Name', required=True)
    email = forms.EmailField(label='Email', required=True)
    number = forms.CharField(label='Phone Number', required=True)
    subject = forms.CharField(label='Subject', required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Contact
        fields = [
            'name',
            'email',
            'number',
            'subject',
            'message'
        ]
