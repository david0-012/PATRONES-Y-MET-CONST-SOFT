from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from ..blogs.forms import RegisterForm
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.views import View    
from django.utils.encoding import force_str
from django.shortcuts import redirect
from .token import account_activation_token
from django.contrib.auth.views import LoginView as AuthLoginView
UserModel = get_user_model()


class UserRegistration(FormView):
    template_name = 'users/registration.html'
    form_class = RegisterForm
    success_url = reverse_lazy('users:success')#blogs:success
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Deactivate account till it is confirmed
        user.save()

        current_site = get_current_site(self.request)
        mail_subject = 'Activate your account.'
        message = render_to_string('users/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(mail_subject, message, to=[to_email])
        if email.send():
            messages.success(self.request, f'Estimado/a {user}, vaya a la bandeja de entrada de su correo electrónico {to_email} y haga clic en \
                el enlace de activación recibido para confirmar y completar el registro. Nota: revisa tu carpeta de spam.')
        else:
            messages.error(self.request, f'Problem sending email to {to_email}, check if you typed it correctly.')

        return super(UserRegistration, self).form_valid(form)
class AccountVerification(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = UserModel.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                messages.success(request, 'Tu cuenta ha sido activada exitosamente, ahora puedes iniciar sesión')
                return redirect('login')
            else:
                messages.error(request, 'El enlace de activación es inválido')
                return redirect('login')
        except(TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            messages.error(request, 'El enlace de activación es inválido')
            return redirect('login')    
class LoginView(AuthLoginView):
    def get(self, request, *args, **kwargs):
        message = request.session.pop('account_activation_message', None)
        if message:
            messages.success(request, message)
        return super().get(request, *args, **kwargs)      