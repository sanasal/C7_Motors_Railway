#views.py
from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth import login , logout
from .forms import Customers_Data , CustomUserCreationForm
from .models import *
from django.http import HttpResponse , JsonResponse , HttpResponseBadRequest 
from django.template import Template , Context
import json  
import stripe
from django.conf import settings
from django.views import View
import os
from django.http import JsonResponse
from .utils.google_sheets import write_sheet_data
from django.http import FileResponse, HttpResponseNotFound
import os

        
def home(request):
    '''Display the home page'''
    cars = Car.objects.all()
 
    models_years = []
    for car in cars:
        if car.model_year not in models_years:
            models_years.append(car.model_year)

    cars_brands = []
    for car in cars:
        if car.brand_name not in cars_brands:
                cars_brands.append(car.brand_name) 

    context = {
        'cars': cars,
        'models_years':models_years,
        'cars_brands':cars_brands,
    }

    return render(request, 'home.html', context)

def inventory(request):
    '''Display the cars page with optional filtering by type'''

    # Start with all cars
    cars = Car.objects.all()

    context = {
        'cars': cars,
    }

    return render(request, 'inventory.html', context)

def financing(request):
    '''Display the cars page with optional filtering by type'''

    cars = Car.objects.all()
    form = Customers_Data()

    context = {
        'cars': cars,
        'form': form,
    }

    if request.method == 'POST':
        try:
            body = json.loads(request.body) if request.content_type == 'application/json' else request.POST

            car_price = float(body.get('car_price', 0))
            downpayment = float(body.get('downpayment', 0))
            loan_duration = int(body.get('loan_duration', 1))
            action = body.get('action', "")  # Determine which button was clicked



            monthly_interest = ((car_price * 4)/100) / 12

            total_price = car_price + (monthly_interest*loan_duration)

            estimated_monthly_payment = (total_price - downpayment) / loan_duration

            return JsonResponse({
                'estimated_monthly_payment': f"AED {estimated_monthly_payment:.2f}",
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'GET':
        return render(request, "financing.html" , context)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def add_customers_data(request):
    '''Add the customers data to CustomersData model'''
    if request.method == 'POST':
        print("== POST data received ==")
        print(request.POST)  # Show posted data

        form = Customers_Data(request.POST)

        if form.is_valid():
            print("== Form is valid! Saving... ==")
            form.save()
            return redirect('c7_motors:financing')
        else:
            print("== Form is INVALID ==")
            print(form.errors)  # Show why it failed

            cars = Car.objects.all()
            return render(request, 'financing.html', {'form': form, 'cars': cars})

    print("== Not a POST request, redirecting ==")
    return redirect('c7_motors:financing')


def articles(request):
    "Display the articles in the articles page"
    articles = Article.objects.all()

    context = {
        'articles' : articles
    }

    return render(request , 'articles.html' , context)



def contact_us(request):
    '''Display the contact us page'''

    return render(request , 'contact_us.html' )

def about(request):
    '''Display the about page'''

    return render(request , 'about.html')



def cars(request, car_type=None):
    '''Display the cars page with optional filtering by type'''

    # Start with all cars
    cars = Car.objects.all()

    # Filter by type if provided in the URL
    if car_type:
        cars = cars.filter(type=car_type)

    context = {
        'cars': cars,
        'car_type' : car_type
    }

    return render(request, 'cars.html', context)




def cars_search(request):
    '''Filter cars based on search criteria and display them on cars.html'''

    # Retrieve filter parameters
    year = request.GET.get('year')
    brand = request.GET.get('brand')
    style = request.GET.get('style')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')

    # Start with all cars
    cars = Car.objects.all()

    # Apply filters
    if year:
        cars = cars.filter(model_year=year)
    if brand:
        cars = cars.filter(brand_name__icontains=brand)
    if style:
        cars = cars.filter(type__exact=style)
    if price_from and price_to:
        cars = cars.filter(cash_price__range=(price_from,price_to))

    return render(request, 'cars.html', {'cars': cars})

def car_details(request, car_name, car_model, car_id):
    """Display the details of a car based on brand_name, model, and id."""

    try:
        # Retrieve the car object matching the parameters
        car = Car.objects.get(brand_name=car_name, model=car_model, id=car_id)
    except Car.DoesNotExist:
        # Return a 404 response if the car doesn't exist
        return HttpResponseNotFound("Car not found")
    except Car.MultipleObjectsReturned:
        # Handle cases where multiple cars match the query
        return HttpResponseBadRequest("Multiple cars with the same name and model found")
    except ValueError:
        # Handle invalid `car_id`
        return HttpResponseBadRequest("Invalid ID")

    # Fetch all images related to the car
    car_images = car.images.all()

    description_lines = car.description.splitlines()

    context = {
        'description_lines': description_lines,
        'car': car,
        'car_images': car_images,  # Pass images to the template
    }

    return render(request, 'car_details.html', context)

          


def sign_in(request):
    '''Sign in the website for new users'''
    if request.method =='POST':   
        form = CustomUserCreationForm(request.POST)
        if form.is_valid(): 
            user = form.save()              
            #log the user in
            login(request , user)           
            return redirect('c7_motors:home')
    else:           
       form = CustomUserCreationForm()     
    return render(request, 'sign in.html' , {'form' : form})

def log_in(request):
    '''Log in the website for old users'''
    if request.method == 'POST' :   
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request , user)
            if 'next' in request.POST :
                return redirect(request.POST.get('next'))
            else: 
                return redirect ('c7_motors:home')
    else:
        form = AuthenticationForm()
    return render (request , 'log in.html' , {'form':form})

def log_out(request):
    '''Go outside the website'''
    if request.method == 'POST':
        logout(request)   
        return redirect ('c7_motors:home')