#views.py
from django.shortcuts import render , redirect 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login , logout
from .forms import CustomUserCreationForm , RequestsForm , RequestsForm
from .models import *
from django.http import JsonResponse , HttpResponseBadRequest , HttpResponseNotFound
import json  
import urllib
from django.utils import translation
from django.shortcuts import redirect
from c7_motors import settings 
from django.shortcuts import get_object_or_404

def switch_language(request, lang_code):
    """
    Switch site language dynamically when user selects a language.
    """
    # تفعيل اللغة الجديدة
    translation.activate(lang_code)

    # حفظها في session
    request.session['django_language'] = lang_code

    # حفظها في cookies أيضاً
    response = redirect(request.META.get('HTTP_REFERER', '/'))
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)

    return response


        
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


def contact_us(request):
    '''Display the contact us page'''

    return render(request , 'contact_us.html')


def about(request):
    '''Display the about page'''

    return render(request , 'about.html')


def articles(request):
    "Display the articles in the articles page"
    articles = Article.objects.all()

    context = {
        'articles' : articles
    }

    return render(request , 'articles.html' , context)


def financing(request):
    '''Display the cars page with optional filtering by type'''

    cars = Car.objects.all()
    form = RequestsForm()

    context = {
        'cars': cars,
        'form': form,
    }

    return render(request,'financing.html',context)


def get_it_now(request , car_id):
    '''Get It Now Request'''

    car = Car.objects.get(id=car_id)

    context = {'car':car}

    return render(request , 'get_it_now.html' , context)



def add_financing_request_data(request):
    if request.method == 'POST':

        form = RequestsForm(request.POST)

        if form.is_valid():
            # Save to database
            financing_request = form.save()
            
             # Send to WhatsApp
            phone_number = "963956626427"   
            message = (
                f"Car: {financing_request.car}\n"
                f"Name: {financing_request.name}\n"
                f"Phone: {financing_request.mobile_phone}\n"
                f"Payment Method: {financing_request.payment_method}\n"
                f"Language: {financing_request.language}\n"
            ) 
            encoded_message = urllib.parse.quote(message)
            whatsapp_url = f"https://wa.me/{phone_number}?text={encoded_message}"

            return redirect(whatsapp_url)

        else:
            cars = Car.objects.all()
            return render(request, 'financing.html', {'cars': cars, 'form': form})

    return redirect('c7_motors:financing')


def add_request_data(request):
    '''Add the get it now request data to CustomersData model'''
    if request.method == 'POST':              

        form = RequestsForm(request.POST)

        if form.is_valid():
            # Save to database
            financing_request = form.save()
             # Send to WhatsApp
            phone_number = "963956626427"   
            message = (
                f"Car: {financing_request.car}\n"
                f"Name: {financing_request.name}\n"
                f"Phone: {financing_request.mobile_phone}\n"
                f"Payment Method: {financing_request.payment_method}\n"
                f"Language: {financing_request.language}\n"
            ) 
            encoded_message = urllib.parse.quote(message)
            whatsapp_url = f"https://wa.me/{phone_number}?text={encoded_message}"

            return redirect(whatsapp_url)

        else:
            cars = Car.objects.all()
            return render(request, 'get_it_now.html', {'cars': cars, 'form': form})

    return redirect('c7_motors:get_it_now')





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

def car_details(request, car_slug):
    """Display the details of a car based on brand_name, model, and id."""

    try:
        # Retrieve the car object matching the parameters
        car = get_object_or_404(Car,slug=car_slug)
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
        'car_images': car_images,
        'technical_features': car.technical_features.all(),
        'extra_features': car.extra_features.all(), 
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