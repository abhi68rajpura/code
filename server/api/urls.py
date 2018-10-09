from django.conf.urls import *
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
	
	path('',views.index,name="index"),
	path('getAllData',views.getAllData,name="getAllData"),
	path('getDiff',views.getDiff,name="getDiff"),
	path('getSettings',views.getSettings,name="getSettings"),
	path('postSettings',views.postSettings,name="=postSettings"),
	path('login',views.login,name="login"),
	path('checkLogin',views.checkLogin,name="checkLogin"),
	path('cuser',views.createUser,name="cuser"),
	
]

