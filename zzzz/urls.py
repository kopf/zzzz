from captcha.fields import ReCaptchaField
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.forms import ValidationError
from registration.backends.default.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail
import requests

from api import v1 as api_v1
from frontend import views as frontend_views
from zzzz.settings import blacklists


class CustomUniqueEmailRegistrationForm(RegistrationFormUniqueEmail):

    captcha = ReCaptchaField(attrs={'theme' : 'clean'})

    def __init__(self, *args, **kwargs):
        super(CustomUniqueEmailRegistrationForm, self).__init__(*args, **kwargs)

        def is_disposable(email):
            msg = ("Unfortunately you'll need to sign up using a real"
                   " (non-disposable) email address. This is simply to"
                   " prevent abuse of the service. You will not be spammed,"
                   " nor will your email address be provided to third parties.")
            domain = email.split('@')[-1].lower()

            if '+' in email and ('gmail.' in domain or 'googlemail.' in domain):
                raise ValidationError(msg)
            if domain in blacklists.EMAIL_DOMAINS:
                raise ValidationError(msg)

            try:
                result = requests.get('https://www.mogelmail.de/q/{0}'.format(domain))
            except:
                pass
            else:
                if result and result.text == '1':
                    raise ValidationError(msg)

        def must_contain_one_at_sign(email):
            """Filter email addresses without an @ or with multiple @ signs"""
            if email.count('@') != 1:
                raise ValidationError("Invalid email address.")

        self.fields['email'].validators = [must_contain_one_at_sign, is_disposable]


    def clean_email(self, *args, **kwargs):
        """Normalize cleaned email address to a canonical gmail address, if on gmail"""
        if '@' not in self.cleaned_data['email']:
            raise ValidationError("Invalid email address.")
        email_user, domain = self.cleaned_data['email'].lower().split('@')
        if 'gmail.' in domain or 'googlemail.' in domain:
            email_user = email_user.replace('.', '')
            self.cleaned_data['email'] = '{}@{}'.format(email_user, 'gmail.com')
        return super(CustomUniqueEmailRegistrationForm, self).clean_email(*args, **kwargs)


class CustomEmailRestrictionsView(RegistrationView):
    form_class = CustomUniqueEmailRegistrationForm


admin.autodiscover()
urlpatterns = [
    url(r'^$', frontend_views.index, name='frontend.views.index'),
    url(r'^faq/$', frontend_views.faq, name='frontend.views.faq'),
    url(r'^donate/$', frontend_views.donate, name='frontend.views.donate'),
    url(r'^api/v1/create/', api_v1.create, name='api.v1.create'),
    url(r'^api/v1/reset_token/', api_v1.reset_token, name='api.v1.reset_token'),
    url(r'^api/v1/update/(?P<subdomain>[-\w]+).zzzz.io/', api_v1.update),
    url(r'^api/v1/update/(?P<subdomain>[-\w]+)/', api_v1.update, name='api.v1.update'),
    url(r'^api/v1/delete/(?P<subdomain>[-\w]+).zzzz.io/', api_v1.delete),
    url(r'^api/v1/delete/(?P<subdomain>[-\w]+)/', api_v1.delete, name='api.v1.delete'),
    url(r'^account/password/change/$', auth_views.password_change,
        name='password_change'),
    url(r'^account/password/change/done/$', auth_views.password_change_done,
        name='password_change_done'),
    url(r'^account/password/reset/$', auth_views.password_reset,
        name='password_reset'),
    url(r'^account/password/reset/done/$', auth_views.password_reset_done,
        name='password_reset_done'),
    url(r'^account/password/reset/complete/$', auth_views.password_reset_complete,
        name='password_reset_complete'),
    url(r'^account/password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^account/register/$', RedirectView.as_view(url='/'),
        name='registration_register'),
    url(r'^account/', include('registration.urls')),
    url(r'^account/modify/$', frontend_views.modify_account, name='frontend.views.modify_account'),
    url(r'^account/delete/$', frontend_views.delete_account, name='frontend.views.delete_account'),
    url(r'^account/export/json/$', frontend_views.export_account_json, name='frontend.views.export_account_json'),
    url(r'^account/$', frontend_views.account, name='frontend.views.account'),
    url(r'^www.zzzz.io.html$', frontend_views.startssl_validation_code),
    url(r'^zzzz.io.html$', frontend_views.startssl_validation_code),
    url(r'^admin/', include(admin.site.urls))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
