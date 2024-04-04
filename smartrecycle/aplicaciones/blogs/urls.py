from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView
app_name = 'blogs'

urlpatterns = [
    path('foro/', views.home_page, name='foro'),
    path('post/<slug:slug>', views.PostView.as_view(), name='post'),
    path('featured/', views.FeaturedListView.as_view(), name='featured'),
    path('category/<slug:slug>', views.CategoryListView.as_view(), name='category'),
    path('search/', views.SearchResultsView.as_view(), name='search'),
    #Registration
    path('registration/', views.UserRegistration.as_view(), name='registration'),
    path('success/',TemplateView.as_view(template_name='users/success_registration.html'), name='success')
    
    
]

