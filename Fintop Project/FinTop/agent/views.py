from django.shortcuts import render

# Create your views here.
class SignUpView(View):
    form_class = SignUpForm

    template_name = 'account/signup.html'

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
                user.is_active = False  # Deactivate account till it is confirmed
                user.save()
                reff = Referral(referred_by_id=uid, user_id=user.pk)
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
                    user=user, phnumber=phnumber, email_confirmed=False)
                new_profile.save()
                current_site = get_current_site(request)
                subject = 'Activate Your FinTop Account'
                message = render_to_string('emails/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                user.email_user(subject, message)
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
            return redirect('dashboard_home')
        else:
            messages.warning(
                request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('dashboard_home')
