from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError

from .forms import SignUpForm
from django.views.generic import View, UpdateView
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from user.tokens import account_activation_token
from user.models import Referral, Profile
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.contrib.auth import login, authenticate
from .forms import KYCForm, KycFormprimary, KycFormsecondary, KycMemberForm
from .models import Kyc
from user.models import Referral, Business, Verification, BankInfo, Loan, Profile, Additional_assets, \
    Additional_liabilities, Contact, Underprocess_loans


# Create your views here.

class SignUpVieww(View):
    form_class = SignUpForm

    template_name = 'account/signup_agent.html'

    @classmethod
    def ref(self, request, uid, *args, **kwargs):
        form = self.form_class()
        # link = request.GET.get('ref=', None)
        return render(request, self.template_name, {'form': form, 'uid': uid})

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():

            emaill = form.cleaned_data['email']
            if User.objects.filter(email=emaill).exists():

                return HttpResponse('User with same email already exists, Please try again with different Username!!')
            else:

                user = form.save(commit=False)
                ph = list(form.cleaned_data['phnumber'])
                if ph[0] is "+":
                    phnumber = ''.join(map(str, ph))
                else:
                    if ph[0] is "0":
                        ph.pop(0)
                        ph.insert(0, "1")
                        ph.insert(0, "6")
                        ph.insert(0, "+")
                        phnumber = ''.join(map(str, ph))
                    else:
                        ph.insert(0, "1")
                        ph.insert(0, "6")
                        ph.insert(0, "+")
                        phnumber = ''.join(map(str, ph))
                user.is_active = True  # Deactivate account till it is confirmed
                user.is_agent = True
                user.save()
                new_profile = Profile(
                    user=user, phnumber=phnumber, email_confirmed=False, is_agent=True)
                new_profile.save()
                current_site = get_current_site(request)
                subject = 'Activate Your FinTop Account'
                message = render_to_string('emails/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                # user.email_user(subject, message)

                messages.success(
                    request, ('Please check your mail for complete registration.'))

                # return redirect('login')

                return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, {'form': form})


class SignUpView(View):
    form_class = SignUpForm

    template_name = 'account/signup_agent.html'

    @classmethod
    def ref(self, request, uid, *args, **kwargs):
        form = self.form_class()
        # link = request.GET.get('ref=', None)
        return render(request, self.template_name, {'form': form, 'uid': uid})

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        print(User.objects.all())
        return render(request, self.template_name, {'form': form})

    def post(self, request, uid, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            emaill = form.cleaned_data['email']
            if User.objects.filter(email=emaill).exists():

                return HttpResponse('User with same email already exists, Please try again with different Username!!')
            else:
                user = form.save(commit=False)
                user.is_active = True  # Deactivate account till it is confirmed
                user.is_agent = True
                user.save()

                comm = 0
                comm_status = "done"
                reff = Referral(referred_by_id=uid, user_id=user.pk, commissions=comm,
                                commission_status=comm_status)

                reff.save()
                ph = list(form.cleaned_data['phnumber'])
                if ph[0] is "+":
                    phnumber = ''.join(map(str, ph))
                else:
                    if ph[0] is "0":
                        ph.pop(0)
                        ph.insert(0, "1")
                        ph.insert(0, "6")
                        ph.insert(0, "+")
                        phnumber = ''.join(map(str, ph))
                    else:
                        ph.insert(0, "1")
                        ph.insert(0, "6")
                        ph.insert(0, "+")
                        phnumber = ''.join(map(str, ph))
                new_profile = Profile(
                    user=user, phnumber=phnumber, email_confirmed=False, is_agent=True)
                new_profile.save()
                current_site = get_current_site(request)
                subject = 'Activate Your FinTop Account'
                message = render_to_string('emails/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                # user.email_user(subject, message)
                messages.success(
                    request, ('Please check your mail for complete registration.'))
                # return redirect('login')
                return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, {'form': form})


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True

            pr = Profile.objects.get(user=user)
            pr.email_confirmed = True
            pr.save()
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return HttpResponse('Your account have been confirmed.')
        else:
            messages.warning(
                request, ('The confirmation link was invalid, possibly because it has already been used.'))
            # return redirect('dashboard_home')
            return HttpResponse('The confirmation link was invalid, possibly because it has already been used.')


def login_agent(request):
    if request.user.is_authenticated:
        pr = Profile.objects.get(user=request.user)
        if pr.is_agent:
            print(request.user)
            return redirect('agent:agent_home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('pass')

            print(username)
            print(password)
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                pr = Profile.objects.get(user=user)
                if pr.is_agent:
                    login(request, user)
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    else:
                        return redirect('agent:agent_home')
                else:
                    messages.info(request, 'This Agent Login')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}

        return render(request, 'account/login_agent.html', context)


def agent_dashboard(request):
    user = request.user
    pr = Profile.objects.get(user=user)
    if pr.kyc_done:
        return render(request, 'agent/home.html')
    else:
        return redirect('agent:kyc')


def KycForm(request):
    if request.method == 'POST':
        f1 = KYCForm(request.POST)
        f2 = KycFormprimary(request.POST or None, request.FILES or None)
        f3 = KycFormsecondary(request.POST or None, request.FILES or None)
        f4 = KycMemberForm(request.POST or None, request.FILES or None)
        print(f2.files)
        try:
            f2_document = request.FILES['document']
        except MultiValueDictKeyError:
            f2_document = False
        try:
            f3_document = request.FILES['Sdocument']
        except MultiValueDictKeyError:
            f3_document = False
        try:
            f4_document = request.FILES['Diploma_certificate']
        except MultiValueDictKeyError:
            f4_document = False
        print(f2_document, f3_document, f4_document)
        user = request.user
        if f1.is_valid():
            print("f1 is valid")
            fo1 = f1.save(commit=False)
            fo1.user = user
            fo1.save()
        if f2.is_valid():

            # if f2_document:
            #     print('f2 is valid')
            #     fo2 = f2.data['name_of_document']
            #     print(fo2)
            foo2 = f2.save(commit=False)
            fu = Kyc.objects.get(user=user)
            foo2.kyc = fu
            # foo2.document=fo2
            if foo2.name_of_document == 'Foreign Passport (current)' or 'Australian Passport (current or expired within last 2 years but not cancelled)' or 'Australian Citizenship Certificate' or 'Full Birth certificate (not birth certificate extract)' or 'Certificate of Identity issued by the Australian Government to refugees and non Australian citizens for entry to Australia':
                foo2.points = 70
            else:
                foo2.points = 40
            foo2.save()
        if f3.is_valid():
            fo3 = f3.save(commit=False)
            fu = Kyc.objects.get(user=user)
            fo3.kyc = fu
            if fo3.name_of_Sdocument == 'Department of Veterans Affairs (DVA) card' or 'Centrelink card (with reference number)':
                fo3.points = 40
            elif fo3.name_of_Sdocument == 'Utility Bill - electricity, gas, telephone - Current address (less than 12 months old)' or 'Reference from Indigenous Organisation' or 'Documents issued outside Australia (equivalent to Australian documents).Must have official translation attached':
                fo3.points = 20
            else:
                fo3.points = 25
            fo3.save()
        if f4.is_valid():
            fo4 = f4.save(commit=False)
            fu = Kyc.objects.get(user=user)
            fo4.kyc = fu
            fo4.save()
        pr = Profile.objects.get(user=request.user)
        pr.kyc_done = True
        pr.save()
        return redirect('agent:agent_home')

    f1 = KYCForm()
    f2 = KycFormprimary()
    f3 = KycFormsecondary()
    f4 = KycMemberForm()
    u = request.user
    user = Profile.objects.get(user=request.user)
    return render(request, 'kyc/agent.html', {'f1': f1, 'f2': f2, "f3": f3, 'f4': f4, 'u': user})


def underproccessedLoan(request):
    a = request.user

    u = Underprocess_loans.objects.filter(agent=a).exclude(admin_approve=False)
    return render(request, 'agent/underproccessedLoan.html', {'a': a, 'under': u})