from django import views
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static      
from django.conf import settings    
from . import views      

app_name='c7_motors'

urlpatterns = [          
    path('' , views.home , name='home'),  
    path('search/' , views.cars_search , name='cars_search'),  
    path('about/' , views.about ,name='about'),
    path('inventory/' , views.inventory , name='inventory'),
    path('financing/' , views.financing , name = 'financing'),
    path('articles/' , views.articles , name='articles'),
    path('contact_us/' , views.contact_us , name='contact_us'),
    path('car_details/<slug:car_slug>/' , views.car_details , name='car_details'),
    path('cars/', views.cars, name='cars'),
    path('get_it_now/<int:car_id>/' , views.get_it_now , name='get_it_now'),
    path('cars/<str:car_type>/', views.cars, name='cars_filtered'),
    path('lang/<str:lang_code>/', views.switch_language, name='switch_language'),

    path('log_in/' , views.log_in , name='log_in'),
    path('sign_in/' , views.sign_in , name='sign_in'), 
    path('log_out/' , views.log_out , name='log_out'),  

    path('add_financig_data/' , views.add_financing_request_data , name = 'add_f_request_data'),
    path('add_request_data/' , views.add_request_data , name = 'add_request_data'),
]
