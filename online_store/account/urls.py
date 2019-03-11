from django.urls import path, include
from . import views

app_name = 'account'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup', views.signup, name='signup'),
    # path('create-account', views.create_account, name='create-account'),
    # path('forgot-password', views.forgot_password, name='forgot-password'),
    # path('reset-email-sent', views.reset_email_sent, name='reset-email-sent'),
    # path('profile', views.profile, name='profile'),
    # path('settings', views.settings, name='settings')
]
