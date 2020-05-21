from django.urls import path,include
from . views import *

urlpatterns = [
	path('register',Registers.as_view(),name='register'),
	path('login',LoginView.as_view(),name='login'),
	path('logout',LogoutView.as_view(),name='logout'),
	path('changepassword',ChangePassword.as_view(),name='changepassword'),

	
]
