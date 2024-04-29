from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView
from .views import UserRegistration, AccountVerification
app_name = 'users'

from .views import LoginView
urlpatterns = [
    #Registration
    path('registration/', views.UserRegistration.as_view(), name='registration'),
    path('success/',TemplateView.as_view(template_name='users/success_registration.html'), name='success'),    
    path('register/', UserRegistration.as_view(), name='register'),
    path('verify/<uidb64>/<token>/', AccountVerification.as_view(), name='account_verification'),
    path('login/', LoginView.as_view(), name='login'),   
]
