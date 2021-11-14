from django.contrib import admin
from .models import Kyc_member,Kyc_primary_police,Kyc_secondary_police,Kyc
# Register your models here.
admin.site.register(Kyc)
admin.site.register(Kyc_primary_police)
admin.site.register(Kyc_secondary_police)
admin.site.register(Kyc_member)