from django.contrib import admin
from .models import Referral, User, Loan, BankInfo, Profile, Additional_assets, Additional_liabilities, Verification, Contact
from django.db import models




@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('referred_by', 'user', 'status')
    search_fields = ['referred_by__username']
    pass

class Additional_assetsInline(admin.TabularInline):
    model = Additional_assets
    extra = 0

class Additional_liabilitiesInline(admin.TabularInline):
    model = Additional_liabilities
    extra = 0
    

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('id','user_id',
            'loan_type',
            'loan_wname',
            'loan_wphone',
            'loan_wemail',
            'vehicle',
            'vehicle_worth',
            'vehicle_money',
            'carloan_pay',
            'accounts',
            'superannuation',
            'credit_card',
            'loans',
            'employment_type',
            'annual_salary',
            'monthly_expense')
    inlines = [
        Additional_assetsInline,
        Additional_liabilitiesInline
    ]
    search_fields = ['user_id__username']
    
    
@admin.register(BankInfo)
class BankInfoAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'bankname', 'acno', 'bankisc')
    search_fields = ['user_id__username']
    pass

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phnumber', 'email_confirmed')
    search_fields = ['user__username']
    pass

@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_bizpartner')
    search_fields = ['user__username']
    pass


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name',
            'email',
            'number',
            'subject',
            'message')
    pass
