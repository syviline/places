from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from .utils import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.views import View


def register_request(request):
    if request.user.is_authenticated:
        return redirect('main:index')
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            email = user.email
            user.save()
            # login(request, user)
            current_site = get_current_site(request)
            email_body = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }

            link = reverse('activate', kwargs={
                'uidb64': email_body['uid'], 'token': email_body['token']})

            email_subject = 'Activate your account'

            activate_url = 'http://' + current_site.domain + link

            email = EmailMessage(
                email_subject,
                'Привет ' + user.username + ', перейдите по этой ссылке чтобы подтвердить аккаунт. \n' + activate_url,
                'noreply@none.com',
                [email],
            )
            email.send(fail_silently=False)
            return redirect('mail_confirm')
            # messages.success(request, "Registration successful.")
            # return redirect("main:index")
        #return render(request=request, template_name="registration/signup.html", context={"form": form})
        # messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="registration/signup.html", context={"form": form})


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass
        return redirect('login')


def profile(request):
    return render(request, "accounts/profile.html")


def mail_confirm(request):
    return render(request, 'registration/confirm_your_mail.html')