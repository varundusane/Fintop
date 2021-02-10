from django.contrib import admin
from .models import Referral, User, Loan, BankInfo, Profile, Additional_assets, Additional_liabilities, Verification, Contact, Business
from django.db import models
import os




@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_display = ('user', 'fullname', 'signature','pdf',  'status', 'created_on')
    
    search_fields = ['user__username']
    
    def download_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),f'agreement/some.csv'), 'w+')
        writer = csv.writer(f)

        writer.writerow(['id','user', 'fullname', 'signature', 'pdf', 'pdfurl', 'status', 'created_on'])

        for s in queryset:
            writer.writerow([s.id, s.user, s.fullname, s.signature, s.pdf, s.pdfurl, s.status, s.created_on])

        f.close()

        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),f'agreement/some.csv'), 'r+')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Bizpartner-data.csv'
        return response

    download_csv.short_description = "export csv"

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_display = ('referred_by', 'user', 'status', 'commission_status',  'commissions')
    search_fields = ['referred_by__username']
    
    def download_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),f'agreement/some.csv'), 'w+')
        writer = csv.writer(f)

        writer.writerow(['id','referred_by','user','status','commission_status', 'commissions','created_on'])

        for s in queryset:
            writer.writerow([s.id, s.referred_by, s.user, s.status, s.commission_status, s.commissions, s.created_on])

        f.close()

        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),f'agreement/some.csv'), 'r+')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=referral-info.csv'
        return response

    download_csv.short_description = "export csv"


class Additional_assetsInline(admin.TabularInline):
    model = Additional_assets
    extra = 0

class Additional_liabilitiesInline(admin.TabularInline):
    model = Additional_liabilities
    extra = 0



@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('id','user_id','loan_type','loan_wname','loan_wphone','loan_wemail','vehicle','vehicle_worth','vehicle_money','carloan_pay','accounts','superannuation','credit_card','loans','employment_type','annual_salary','monthly_expense', 'created_on')
    inlines = [
        Additional_assetsInline,
        Additional_liabilitiesInline
    ]
    actions = ['download_csv']
    search_fields = ['user_id__username']

    list_filter = (
        'user_id',
    )

    def download_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),f'agreement/some.csv'), 'w+')
        writer = csv.writer(f)
        writer.writerow(['id','user_id','loan_type','loan_wname','loan_wphone','loan_wemail','vehicle','vehicle_worth','vehicle_money','carloan_pay','accounts','superannuation','credit_card','loans','employment_type','annual_salary','monthly_expense', 'created_on'])

        for s in queryset:
            writer.writerow([s.id, s.user_id, s.loan_type, s.loan_wname, s.loan_wphone, s.loan_wemail, s.vehicle, s.vehicle_worth, s.vehicle_money, s.carloan_pay, s.accounts, s.superannuation, s.credit_card, s.loans, s.employment_type, s.annual_salary, s.monthly_expense, s.created_on])

        f.close()

        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),f'agreement/some.csv'), 'r+')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=loan-info.csv'
        return response

    download_csv.short_description = "export csv"
    
@admin.register(BankInfo)
class BankInfoAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'bankname', 'acno', 'bankisc')
    search_fields = ['user_id__username']
    actions =['download_csv']

    def download_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),f'agreement/some.csv'), 'w+')
        writer = csv.writer(f)
        writer.writerow(['id','user_id','bankname','acname','acno','bankisc','created_on'])

        for s in queryset:
            writer.writerow([s.id, s.user_id, s.bankname, s.acname, s.acno, s.bankisc, s.created_on])

        f.close()

        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),f'agreement/some.csv'), 'r+')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=bank-info.csv'
        return response

    download_csv.short_description = "export csv"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phnumber', 'email_confirmed')
    search_fields = ['user__username']
    actions =['download_csv']

    def download_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

    #     user = models.OneToOneField(User, on_delete=models.CASCADE)
    # phnumber = models.CharField(max_length=20)
    # email_confirmed = models.BooleanField(default=False)
        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),f'agreement/some.csv'), 'w+')
        writer = csv.writer(f)
        writer.writerow(['id','user','phnumber','email_confirmed'])

        for s in queryset:
            writer.writerow([s.id, s.user, s.phnumber, s.email_confirmed])

        f.close()

        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),f'agreement/some.csv'), 'r+')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=profile-info.csv'
        return response

    download_csv.short_description = "export csv"

@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):

    # def is_bizpartner(self):
    #     return self.is_bizpartner=1
    # is_bizpartner = "Yes"

    list_display = ('user', 'is_Bizpartner')

    search_fields = ['user__username']
    actions =['download_csv']

    def is_Bizpartner(self, obj):
        if obj.is_bizpartner=="1":
            is_Bizpartner = "yes "
            return is_Bizpartner
        elif obj.is_bizpartner=="0":
            is_Bizpartner="No"
            return is_Bizpartner
   

    def download_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        
        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),f'agreement/some.csv'), 'w+')
        writer = csv.writer(f)
        writer.writerow(['id','user', 'is_bizpartner'])

        for s in queryset:
            writer.writerow([s.id, s.user, s.is_bizpartner])

        f.close()

        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),f'agreement/some.csv'), 'r+')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=vrification-info.csv'
        return response

    download_csv.short_description = "export csv"


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name',
            'email',
            'number',
            'subject',
            'message',
            'created_on')
    actions =['download_csv']
    search_fields = ['name']

    def download_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),f'agreement/some.csv'), 'w+')
        writer = csv.writer(f)
        writer.writerow(['id','name','email','number','subject','message', 'created_on'])

        for s in queryset:
            writer.writerow([s.id, s.name, s.email, s.number, s.subject, s.message])

        f.close()

        f = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),f'agreement/some.csv'), 'r+')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=inbox-info.csv'
        return response

    download_csv.short_description = "export csv"
