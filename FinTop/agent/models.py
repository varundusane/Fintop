from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User

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


# Create your models here.
class Kyc(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    agentId = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Please enter valid phone number. Correct format is 04XXXXXXXX")
    phone = models.CharField(validators=[phone_regex], max_length=20, blank=True)
    residential_Address = models.TextField()
    communication_address = models.TextField()


class Kyc_primary_police(models.Model):
    kyc = models.ForeignKey(Kyc, on_delete=models.CASCADE)
    name_of_document = models.CharField(max_length=12500, choices=primary_document)
    points = models.IntegerField()
    document = models.FileField(upload_to="AgentKycDocument/")


class Kyc_secondary_police(models.Model):
    kyc = models.ForeignKey(Kyc, on_delete=models.CASCADE)
    name_of_Sdocument = models.CharField(max_length=150, choices=secondary_document)
    points = models.IntegerField()
    Sdocument = models.FileField(upload_to="AgentKycDocument/")


class Kyc_member(models.Model):
    kyc = models.ForeignKey(Kyc, on_delete=models.CASCADE)
    afca_membership = models.CharField(max_length=50)
    Aggregator_contractor = models.CharField(max_length=50)
    Aggregator_ManagerName = models.CharField(max_length=50, blank=True, null=True)
    Aggregator_ManagerNumber = models.CharField(max_length=50, blank=True, null=True)
    ABN_Number = models.CharField(max_length=50, blank=True, null=True)
    Diploma_certificate = models.FileField(upload_to="diploma/")
