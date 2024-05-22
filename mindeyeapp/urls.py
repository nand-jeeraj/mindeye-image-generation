from django.urls import path
from . import views

urlpatterns =[
    
    path('',views.home, name="home"),
    path('generate_image',views.generate_image, name="generate_image"),
    path('signup/',views.signUpPage,name='signup'),
    path('saveform/',views.saveform,name="saveform"),
    path('login/',views.loginPage,name="login"),
    path('loginform/',views.loginSubmit,name="loginsubmit"),
    path('admin/',views.admin,name="admin")
    
]