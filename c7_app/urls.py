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
    path('car_details/<str:car_name>/<str:car_model>/<int:car_id>/' , views.car_details , name='car_details'),
    path('cars/', views.cars, name='cars'),
    path('cars/<str:car_type>/', views.cars, name='cars_filtered'),

    path('log_in/' , views.log_in , name='log_in'),
    path('sign_in/' , views.sign_in , name='sign_in'), 
    path('log_out/' , views.log_out , name='log_out'),  

    path('add_data/' , views.add_customers_data , name = 'add_data'),
]
