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
    path('services/' , views.service , name='service' ),
    path('features/' , views.feature , name='feature' ),
    path('contact_us/' , views.contact_us , name='contact_us'),
    path('car_details/<str:car_name>/<str:car_model>/<int:car_id>/' , views.car_details , name='car_details'),
    path('cars/', views.cars, name='cars'),
    path('cars/<str:car_type>/', views.cars, name='cars_filtered'),
    path('shopping_cart/' , views.shopping_cart , name='shopping_cart'),
    path('payment_in_installments/' , views.payments_in_installments , name='payment_in_installments'),
    path('payment_in_installments_without_downpayment/' , views.payment_in_installments_without_dp , name='payment_in_installments_without_dp'),

    path('log_in/' , views.log_in , name= 'log_in'),
    path('sign_in/' , views.sign_in , name='sign_in'), 
    path('log_out/' , views.log_out , name='log_out'),  
    
    path('add_to_cart/' , views.add_to_cart , name='add'),
    path('delete/' , views.delete_item , name = 'delete'),
    path('calculate_your_salary/' , views.calculate_customer_salary , name = 'calculate_your_salary'),

    path('cash_add_data/' , views.add_customers_data , name = 'cash_add_data'),
    path('deposit_add_data/' , views.add_customers_data , name = 'deposit_add_data'),
    path('add_installments_data/' , views.add_installments_data , name = 'add_installments_data'),
    path('add_installments_data_without_dp/' , views.add_installments_data_without_dp , name = 'add_installments_data_without_dp'),
    
    path('create-cash-checkout-session/', views.create_cash_checkout_session, name='create-cash-checkout-session'),
    path('create-deposit-checkout-session/', views.create_deposit_checkout_session, name='create-deposit-checkout-session'),
    path('create-remaining-checkout-session/', views.create_remaining_checkout_session, name='create-remaining-checkout-session'),
    path('create-installments-checkout-session-dp/', views.create_installments_checkout_session_dp , name='create-installments-checkout-session-dp'),
    path('create-installments-checkout-session/', views.create_installments_checkout_session , name='create-installments-checkout-session'),
    path('C7_payment_success/', views.send_book_data_after_success, name='success'),
    path('C7_remaining_payment_success/', views.remaining_payment_success, name='remaining_success'),
    path('C7_installments_deposit_payment_success_dp/', views.installments_payment_success_dp, name='installments_deposit_success_dp'),
    path('C7_installments_deposit_payment_success/', views.installments_payment_success, name='installments_deposit_success'),
    path('cash_cancel/', views.cash_payment_cancel, name='cash_cancel'),
    path('deposit_cancel/', views.deposit_payment_cancel, name='deposit_cancel'),
    path('remaining_cancel/', views.remaining_payment_cancel, name='remaining_cancel'),
]
