from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import render_to_pdf
from django.core.files import File
from io import BytesIO



def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Verification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_bizpartner = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = 'BizPartner'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phnumber = models.CharField(max_length=20)
    email_confirmed = models.BooleanField(default=False)
    class Meta:
        verbose_name = 'Profile Verification'
    

class Referral(models.Model):
    referred_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    user =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    status = models.CharField(max_length=15, null=True, blank=True)
    commissions = models.CharField(max_length=20)
    commission_status = models.CharField(max_length=20)
    created_on = models.DateTimeField(auto_now_add=True)

    @property
    def get_phone(self):
        return Profile.objects.get(user__id=self.user.id)
    class Meta:
        verbose_name_plural = 'Bizpartner Commissions'    



class BankInfo(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    bankname = models.CharField(max_length=50)
    acname = models.CharField(max_length=50)
    acno = models.CharField(max_length=50)
    bankisc = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)

class Business(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    fullname = models.CharField(max_length=50)
    signature = models.CharField(max_length=50)
    # pdfurl = models.CharField(max_length=500, null=True)
    # added by khushwant singh 
    pdf = models.FileField(upload_to= "BizpartnerAgreement/" ,null=True, blank=True)
    status = models.CharField(max_length=50, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = 'Bizpartner Data'

    def generate_obj_pdf(instance):
     obj = instance
     context = {'fname': obj.fullname, 'sign': obj.signature}
     pdf = render_to_pdf('commons/agreement.html', context)
     filename = f"agreement/{obj.user.username}.pdf"
     obj.pdf.save(filename, File(BytesIO(pdf.content)))

    
class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    loan_status = models.CharField(max_length=15, null=True, blank=True) 
    loan_wname = models.CharField(max_length=15, null=True, blank=True)
    loan_wphone = models.CharField(max_length=20, null=True, blank=True)
    loan_wemail = models.CharField(max_length=40, null=True, blank=True)
    ltype = (("Buy a Home","Buy a Home"),("Refinance","Refinance"))
    loan_type = models.CharField(max_length=15,choices=ltype)
    yesorno = (("Yes","Yes"),("No","No"))
    vehicle = models.CharField(max_length=25,choices=yesorno)
    vehicle_worth = models.CharField(max_length=20, null=True, blank=True)
    vehicle_money = models.CharField(max_length=20, null=True, blank=True)
    carloan_pay = models.CharField(max_length=25,choices=yesorno,blank=True)
    accounts = models.CharField(max_length=20, null=True, blank=True)
    superannuation = models.CharField(max_length=20, null=True, blank=True)
    additional_asset = models.CharField(max_length=25,choices=yesorno)
    home_content = models.CharField(max_length=20, null=True, blank=True)
    credit_card = models.CharField(max_length=25,choices=yesorno)
    credit_limit = models.CharField(max_length=20, null=True, blank=True)
    liability_loan = models.CharField(max_length=25,choices=yesorno)
    loans = models.CharField(max_length=20, null=True, blank=True)
    employment_choice = (("Employee","Employee"),("Self-employed","Self-employed"),("Not working","Not working"))
    employment_type = models.CharField(max_length=50,choices=employment_choice)
    annual_salary = models.CharField(max_length=20, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)  
    monthly_expense = models.CharField(max_length=20, null=True, blank=True)



@receiver(post_save, sender=Loan)
def updateStatus(sender, instance, created, **kwargs):
    
    try:
        loan = Loan.objects.filter(user=User.objects.get(id=instance.user.id)).first()
        print(loan.id)
    except Loan.DoesNotExist:
        return 
    # if (Referral.objects.filter(user=User.objects.get(id=instance.user.id)).update(status=loan.loan_status)):
        Referral.objects.filter(user=User.objects.get(id=instance.user.id)).update(status=loan.loan_status)
    # else:
    #     return None    



class Additional_assets(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='+')
    select_assets = (("Term Deposit" , "Term Deposit"), ("Shares", "Shares"), ("Managed Funds", "Managed Funds"), ("Gifts", "Gifts")) 
    
    types = models.CharField(max_length=35, choices=select_assets)
    description = models.CharField(max_length=25, null=True, blank=True)
    total_value = models.IntegerField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Additional_assets'
        verbose_name_plural = "Additional_assets"
    
    
class Additional_liabilities(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='+')
    liability_types = (("tax debt","tax debt"),("other lines of credit","other lines of credit"))    
    types = models.CharField(max_length=35, choices=liability_types, null=True, blank=True)
    owned = models.CharField(max_length=20, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)

class Contact(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=20)
    number = models.CharField(max_length=20)
    subject = models.CharField(max_length=50)
    message = models.TextField(null=False, blank=False, max_length=2500)
    created_on = models.DateTimeField(auto_now_add=True) 

    class Meta:
        verbose_name_plural = 'Inbox'