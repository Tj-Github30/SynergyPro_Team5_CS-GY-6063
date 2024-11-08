from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
   path('login/', auth_views.LoginView.as_view(template_name='users/registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/registration/logged_out.html'), name='logout'),
      path('signup/' ,views.signup, name='signup'),
    # Add other views like registration here later
]
