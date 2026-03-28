from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path('UserLogin', views.UserLogin, name="UserLogin"),
	       path('UserLoginAction', views.UserLoginAction, name="UserLoginAction"),	   
	       path('Signup', views.Signup, name="Signup"),
	       path('SignupAction', views.SignupAction, name="SignupAction"),
	       path('SingleEmail', views.SingleEmail, name="SingleEmail"),
	       path('SingleEmailAction', views.SingleEmailAction, name="SingleEmailAction"),
	       path('MultiEmail', views.MultiEmail, name="MultiEmail"),
	       path('MultiEmailAction', views.MultiEmailAction, name="MultiEmailAction"),	
	       path('Compose', views.Compose, name="Compose"),
	       path('ComposeAction', views.ComposeAction, name="ComposeAction"),
	       path('ViewEmail', views.ViewEmail, name="ViewEmail"),
]