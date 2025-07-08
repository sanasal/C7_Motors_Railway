#views.py
from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth import login , logout
from .forms import *
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

def download_part(request, part_name):
    file_path = f'/app/media_zips/{part_name}'
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=part_name)
    return HttpResponseNotFound('File not found.')




        
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
  
    try:
        last_customer_data = CustomersData.objects.filter(user=request.user).order_by('-id').first()
        remaining_price = last_customer_data.remaining_amount
    except:
        remaining_price = 0

    try:
        stripe_remaining = remaining_price
    except:
        stripe_remaining = 0

    context = {
        'stripe_remaining': stripe_remaining,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLIC_KEY,
        'cars': cars,
        'models_years':models_years,
        'cars_brands':cars_brands,
    }

    return render(request, 'home.html', context)


def contact_us(request):
    '''Display the contact us page'''
    
    try:
        last_customer_data = CustomersData.objects.filter(user=request.user).order_by('-id').first()
        remaining_price = last_customer_data.remaining_amount
    except:
        remaining_price = 0

    try:
        stripe_remaining = remaining_price
    except:
        stripe_remaining = 0

    context = {
        'stripe_remaining': stripe_remaining,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLIC_KEY,
    }

    return render(request , 'contact_us.html' , context)

def service(request):
    '''Display the services page'''
    try:
        last_customer_data = CustomersData.objects.filter(user=request.user).order_by('-id').first()
        remaining_price = last_customer_data.remaining_amount
    except:
        remaining_price = 0

    try:
        stripe_remaining = remaining_price
    except:
        stripe_remaining = 0

    context = {
        'stripe_remaining': stripe_remaining,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLIC_KEY,
    }

    return render(request , 'service.html' , context)

def feature(request):
    '''Display the features page'''
    try:
        last_customer_data = CustomersData.objects.filter(user=request.user).order_by('-id').first()
        remaining_price = last_customer_data.remaining_amount
    except:
        remaining_price = 0

    try:
        stripe_remaining = remaining_price
    except:
        stripe_remaining = 0

    context = {
        'stripe_remaining': stripe_remaining,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLIC_KEY,
    }

    return render(request , 'feature.html' , context)

def about(request):
    '''Display the about page'''
    try:
        last_customer_data = CustomersData.objects.filter(user=request.user).order_by('-id').first()
        remaining_price = last_customer_data.remaining_amount
    except:
        remaining_price = 0

    try:
        stripe_remaining = remaining_price
    except:
        stripe_remaining = 0

    context = {
        'stripe_remaining': stripe_remaining,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLIC_KEY,
    }

    return render(request , 'about.html' , context)

@login_required(login_url='/log_in/')
def shopping_cart(request):
    '''Display the shopping cart page'''
    cart = None        
    cartitems = []

    if request.user.is_authenticated:
        cart , created = Cart.objects.get_or_create(user =request.user , completed = False)
        cartitems = cart.cartitems.all()

    try:
        stripe_total_price = cart.total_price()  # Assuming the price is in AED
        stripe_deposit = int(3000)
    except:
        stripe_total_price = 0
        stripe_deposit = 0

    context = {
        'cart' : cart , 
        'items':cartitems,
        'stripe_total_price':stripe_total_price,
        'stripe_deposit' : stripe_deposit,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLIC_KEY,
    }

    return render(request , 'shopping_cart.html' , context)

def payments_in_installments(request):
    '''Display payment in installments with downpayment page and save customer data to InstallmentsCustomer model'''
    cart = None        
    cartitems = []

    if request.user.is_authenticated:
        cart , created = Cart.objects.get_or_create(user =request.user , completed = False)
        cartitems = cart.cartitems.all()

    try:
        stripe_deposit = int(3000)
    except:
        stripe_deposit = 0

    context = {
        'cart' : cart , 
        'items':cartitems,
        'stripe_deposit' : stripe_deposit,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLIC_KEY,
    }

    return render(request , 'payment_in_installments.html' , context)

def payment_in_installments_without_dp(request):
    '''Display payment in installments with downpayment page and save customer data to InstallmentsCustomer model'''
    cart = None        
    cartitems = []

    if request.user.is_authenticated:
        cart , created = Cart.objects.get_or_create(user =request.user , completed = False)
        cartitems = cart.cartitems.all()

    try:
        stripe_deposit = int(3000)
    except:
        stripe_deposit = 0

    context = {
        'cart' : cart , 
        'items':cartitems,
        'stripe_deposit' : stripe_deposit,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLIC_KEY,
    }

    return render(request , 'payment_in_installments_without_dp.html' , context)

def cars(request, car_type=None):
    '''Display the cars page with optional filtering by type'''

    # Start with all cars
    cars = Car.objects.all()

    # Filter by type if provided in the URL
    if car_type:
        cars = cars.filter(type=car_type)

    # Retrieve customer data (if available)
    try:
        last_customer_data = CustomersData.objects.filter(user=request.user).order_by('-id').first()
        remaining_price = last_customer_data.remaining_amount
    except:
        remaining_price = 0

    context = {
        'stripe_remaining': remaining_price,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLIC_KEY,
        'cars': cars,
        'car_type' : car_type
    }

    return render(request, 'cars.html', context)




def cars_search(request):
    '''Filter cars based on search criteria and display them on cars.html'''

    # Retrieve filter parameters
    year = request.GET.get('year')
    brand = request.GET.get('brand')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    KM_from = request.GET.get('KM_from')
    KM_to = request.GET.get('KM_to')

    # Start with all cars
    cars = Car.objects.all()

    # Apply filters
    if year:
        cars = cars.filter(model_year=year)
    if brand:
        cars = cars.filter(brand_name__icontains=brand)
    if price_from and price_to:
        cars = cars.filter(cash_price__range=(price_from,price_to))
    if KM_from and KM_to:
        cars = cars.filter(mileage__range=(KM_from,KM_to))

    return render(request, 'cars.html', {'cars': cars})

def car_details(request, car_name, car_model, car_id):
    """Display the details of a car based on brand_name, model, and id."""
    try:
        last_customer_data = CustomersData.objects.filter(user=request.user).order_by('-id').first()
        remaining_price = last_customer_data.remaining_amount
    except:
        remaining_price = 0

    try:
        stripe_remaining = remaining_price
    except:
        stripe_remaining = 0

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
        'stripe_remaining': stripe_remaining,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLIC_KEY,
        'description_lines': description_lines,
        'car': car,
        'car_images': car_images,  # Pass images to the template
    }

    return render(request, 'car_details.html', context)





def add_customers_data(request):
    '''Add the customers data to CustomersData model'''
    if request.method == 'POST':
        # Determine the payment type (deposit or full)
        payment_type = request.POST.get('payment_type', 'deposit')  # Default to 'deposit'

        form = forms.CustomersData(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user

            # Get the cart and associated cars
            cart = Cart.objects.filter(user=request.user, completed=False).first()
            if cart:
                # Get all cars in the cart
                cars_in_cart = CarsCart.objects.filter(cart=cart)
                car_names = [f"{car_item.car.brand_name} {car_item.car.model}" for car_item in cars_in_cart]  # Extract brand and model names
                instance.cars = ', '.join(car_names)  # Save car names as comma-separated string
                instance.total_amount = cart.total_price()  # Get total price from the cart
            else:
                return JsonResponse({'success': False, 'error': 'Cart not found.'}, status=404)

            if payment_type == 'deposit':
                # Handle deposit payment
                payment_amount = request.POST.get('payment_amount', '3000')  # Default to 3000 if missing
                try:
                    deposit_amount = float(3000)
                    instance.paid_amount = deposit_amount
                    instance.remaining_amount = max(0, instance.total_amount - deposit_amount)
                except ValueError:
                    return JsonResponse({'success': False, 'error': 'Invalid deposit amount.'}, status=400)
            elif payment_type == 'full':
                # Handle full payment
                instance.paid_amount = instance.total_amount  # Paid full amount
                instance.remaining_amount = 0  # No remaining amount

            # Save the instance
            instance.save()

            return JsonResponse({
                'success': True,
                'total_price': instance.total_amount,
                'paid_amount': instance.paid_amount,
                'remaining_amount': instance.remaining_amount
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)

def add_payment_data(request):
    '''See if the payment is cash or deposit'''
    if request.method == "POST":
        try:
            payment_type = request.POST.get('payment_type')
            payment_amount = request.POST.get('payment_amount', '0')  # Default to 0 if missing

            try:
                payment_amount = float(payment_amount)  # Convert payment amount to float
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid payment amount.'}, status=400)

            # Get the current user and their customer data
            customer_data = CustomersData.objects.filter(user=request.user).first()

            if customer_data:
                if payment_type == 'full':
                    # Full payment scenario
                    customer_data.paid_amount = customer_data.total_amount
                    customer_data.remaining_amount = 0
                elif payment_type == 'deposit':
                    # Deposit payment scenario
                    customer_data.paid_amount += 3000
                    customer_data.remaining_amount = max(0, customer_data.total_amount - customer_data.paid_amount)
                else:
                    return JsonResponse({'success': False, 'error': 'Invalid payment type.'}, status=400)

                # Save the updated customer data
                customer_data.save()

                return JsonResponse({
                    'success': True,
                    'paid_amount': customer_data.paid_amount,
                    'remaining_amount': customer_data.remaining_amount
                })
            else:
                return JsonResponse({'success': False, 'error': 'Customer data not found.'}, status=404)
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid payment amount.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)

def add_installments_data(request):
    """Update InstallmentsCustomer with additional details"""
    if request.method == 'POST':
        form = forms.Installments_CustomersData(request.POST, request.FILES)

        if form.is_valid():
            # Fix: Get the first record instead of get_or_create() to avoid duplicate errors
            instance = InstallmentsCustomer.objects.filter(user=request.user).first()
            if not instance:
                instance = InstallmentsCustomer.objects.create(user=request.user)

            # Updating instance fields
            instance.name = form.cleaned_data.get('name', instance.name)
            instance.email = form.cleaned_data.get('email', instance.email)
            instance.mobile_phone = form.cleaned_data.get('mobile_phone', instance.mobile_phone)

            # Handling file uploads safely
            for field in ['passport', 'driver_license', 'personal_identification_card', 
                          'salary_certificate', 'bank_statement']:
                file = request.FILES.get(field)
                if file:
                    setattr(instance, field, file)

            instance.pick_up_location = form.cleaned_data.get('pick_up_location', instance.pick_up_location)
            instance.pick_up_date = form.cleaned_data.get('pick_up_date', instance.pick_up_date)
            instance.pick_up_time = form.cleaned_data.get('pick_up_time', instance.pick_up_time)

            instance.save()

            return JsonResponse({'success': True, 'message': 'Installments data updated successfully!'})

        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)



def add_installments_data_without_dp(request):
    """Update InstallmentsCustomerWithoutDP with additional details"""
    if request.method == 'POST':
        form = forms.Installments_CustomersData_Without_DP(request.POST, request.FILES)

        if form.is_valid():
            # Fix: Get the first record instead of get_or_create() to avoid duplicate errors
            instance = InstallmentsCustomerWithoutDP.objects.filter(user=request.user).first()
            if not instance:
                instance = InstallmentsCustomerWithoutDP.objects.create(user=request.user)

            # Updating instance fields
            instance.name = form.cleaned_data.get('name', instance.name)
            instance.email = form.cleaned_data.get('email', instance.email)
            instance.mobile_phone = form.cleaned_data.get('mobile_phone', instance.mobile_phone)

            # Handling file uploads safely
            for field in ['passport', 'driver_license', 'personal_identification_card', 
                          'salary_certificate', 'bank_statement']:
                file = request.FILES.get(field)
                if file:
                    setattr(instance, field, file)

            instance.pick_up_location = form.cleaned_data.get('pick_up_location', instance.pick_up_location)
            instance.pick_up_date = form.cleaned_data.get('pick_up_date', instance.pick_up_date)
            instance.pick_up_time = form.cleaned_data.get('pick_up_time', instance.pick_up_time)

            instance.save()

            return JsonResponse({'success': True, 'message': 'Installments data updated successfully!'})

        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)




stripe.api_key = settings.STRIPE_SECRET_KEY

def create_cash_checkout_session(request):
    '''Create Stripe checkout page for cash pay'''
    try:
        # Get the request data
        data = json.loads(request.body)

        cart = None        
        cartitems = []
        
        if request.user.is_authenticated:
            cart , created = Cart.objects.get_or_create(user =request.user , completed = False)
            cartitems = cart.cartitems.all()

        # Calculate the total amount using total_price()
        total_amount = int(cart.total_price() * 100) 
    
        # Create the Stripe Checkout session
        checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'AED',  # Adjust currency if needed
                        'product_data': {
                            'name': 'C7 Motors',  # The product description shown on Stripe Checkout
                        },
                        'unit_amount': total_amount,  # The amount in cents
                    },
                    'quantity': 1,
                }],
                mode='payment',  # Single full payment mode
                success_url='https://c7motors.up.railway.app/C7_payment_success/',  # Adjust the URL to your success page
                cancel_url='https://c7motors.up.railway.app/cash_cancel/',  # Adjust the URL to your cancel page
        )

        # Return the session ID as JSON response
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def create_deposit_checkout_session(request):
    '''Create Stripe checkout page for deposit pay'''
    try:
        # Get the request data
        data = json.loads(request.body)

        # Calculate the total amount using total_price()
        total_amount = int(3000 * 100)
            
        # Create the Stripe Checkout session
        checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'AED',  # Adjust currency if needed
                        'product_data': {
                            'name': 'Deposit C7 Motors',  # The product description shown on Stripe Checkout
                        },
                        'unit_amount': total_amount,  # The amount in cents
                    },
                    'quantity': 1,
                }],
                mode='payment',  # Single full payment mode
                success_url='https://c7motors.up.railway.app/C7_payment_success/',  # Adjust the URL to your success page
                cancel_url='https://c7motors.up.railway.app/deposit_cancel/',  # Adjust the URL to your cancel page
        )

        # Return the session ID as JSON response
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def create_remaining_checkout_session(request):
    '''Create Stripe checkout page for remaining price'''
    try:
        try:
            # Get the request data
            last_customer_data = CustomersData.objects.filter(user=request.user).order_by('-id').first()
            total_amount = int(last_customer_data.remaining_amount * 100)
        except:
            total_amount = 0

        # Create the Stripe Checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'AED',  # Adjust currency if needed
                    'product_data': {
                        'name': 'Remaining Price C7 Motors',  # The product description shown on Stripe Checkout
                    },
                    'unit_amount': total_amount,  # The amount in cents
                },
                'quantity': 1,
            }],
            mode='payment',  # Single full payment mode
            success_url='https://c7motors.up.railway.app/C7_remaining_payment_success/',
            cancel_url='https://c7motors.up.railway.app/remaining_cancel/',
        )

        # Return the session ID as JSON response
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def create_installments_checkout_session_dp(request):
    '''Create Stripe checkout page for installments payment pay'''
    try:
        # Get the request data
        data = json.loads(request.body)

        # Calculate the total amount using total_price()
        total_amount = int(3000 * 100)
            
        # Create the Stripe Checkout session
        checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'AED',  # Adjust currency if needed
                        'product_data': {
                            'name': 'Installments C7 Motors',  # The product description shown on Stripe Checkout
                        },
                        'unit_amount': total_amount,  # The amount in cents
                    },
                    'quantity': 1,
                }],
                mode='payment',  # Single full payment mode
                success_url='https://c7motors.up.railway.app/C7_installments_deposit_payment_success_dp/',  # Adjust the URL to your success page
                cancel_url='https://c7motors.up.railway.app/installments_cancel/',  # Adjust the URL to your cancel page
        )

        # Return the session ID as JSON response
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def create_installments_checkout_session(request):
    '''Create Stripe checkout page for installments payment pay'''
    try:
        # Get the request data
        data = json.loads(request.body)

        # Calculate the total amount using total_price()
        total_amount = int(3000 * 100)
            
        # Create the Stripe Checkout session
        checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'AED',  # Adjust currency if needed
                        'product_data': {
                            'name': 'Installments C7 Motors',  # The product description shown on Stripe Checkout
                        },
                        'unit_amount': total_amount,  # The amount in cents
                    },
                    'quantity': 1,
                }],
                mode='payment',  # Single full payment mode
                success_url='https://c7motors.up.railway.app/C7_installments_deposit_payment_success/',  # Adjust the URL to your success page
                cancel_url='https://c7motors.up.railway.app/installments_cancel/',  # Adjust the URL to your cancel page
        )

        # Return the session ID as JSON response
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




def send_book_data_after_success(request):
    '''Send the data to email if the payment is successful and mark the car as sold'''
    customer_book_data = None
    if request.user.is_authenticated:
        customer_book_data = CustomersData.objects.filter(user=request.user).order_by('-id').first()

        # Mark the cart as completed
        cart = Cart.objects.filter(user=request.user, completed=False).first()
        if cart:
            cart.completed = True
            cart.save()
            print(f"Cart {cart.id} marked as completed")  # Debug print
    else:
        print('User is not authenticated')  # Debug print

    if customer_book_data and customer_book_data.cars:
        print(f"Cars field: {customer_book_data.cars}")  # Debug print
        car_names = customer_book_data.cars.split(', ')  # Split the comma-separated string into a list of car names
        for car_name in car_names:
            try:
                # Split the car name into brand and model
                brand_name, model = car_name.split(' ', 1)  # Split on the first space
                car = Car.objects.get(brand_name=brand_name, model=model)  # Fetch the car by brand and model
                print(f"Updating car {car_name} to sold")  # Debug print
                car.selled = True
                car.save()
            except (ValueError, Car.DoesNotExist) as e:
                print(f"Error processing car {car_name}: {e}")  # Debug print
    else:
        print('No customer book data or cars field is empty')  # Debug print

    context = {
       'customer_book_data': customer_book_data
    }

    return render(request, 'success.html', context)

def remaining_payment_success(request):
    """Handle successful payments and updates customer data."""
    try:
        # Update customer data
        if request.user.is_authenticated:
            last_customer_data = CustomersData.objects.filter(user=request.user).order_by('-id').first()
        
            # Assuming `cars` field in `CustomersData` contains the brand and model names of the cars sold
            if last_customer_data and last_customer_data.cars:
                car_names = last_customer_data.cars.split(', ')  # Split the comma-separated string into a list of car names
                for car_name in car_names:
                    try:
                        # Split the car name into brand and model
                        brand_name, model = car_name.split(' ', 1)  # Split on the first space
                        car = Car.objects.get(brand_name=brand_name, model=model)  # Fetch the car by brand and model
                        car.selled = True
                        car.save()
                    except (ValueError, Car.DoesNotExist) as e:
                        print(f"Error processing car {car_name}: {e}")
        
        else:
            print('User is not authenticated')  # Debug print
        
        if not last_customer_data:
            return JsonResponse({'error': 'Customer data not found.'}, status=404)

        # Update payment details
        last_customer_data.paid_amount += last_customer_data.remaining_amount
        last_customer_data.remaining_amount = 0
        last_customer_data.save()

    except Exception as e:
       return JsonResponse({'error': str(e)}, status=500)

    context = {
       'last_customer_data': last_customer_data
    }

    return render(request, 'remaining_success.html', context)

def installments_payment_success_dp(request):
    '''Handle successful payments and updates customer data.'''
    try:
        # Update customer data
        if request.user.is_authenticated:
            last_customer_data = InstallmentsCustomer.objects.filter(user=request.user).order_by('-id').first()

            # Assuming `cars` field in `CustomersData` contains the brand and model names of the cars sold
            if last_customer_data and last_customer_data.cars:
                car_names = last_customer_data.cars.split(', ')  # Split the comma-separated string into a list of car names
                for car_name in car_names:
                    try:
                        # Split the car name into brand and model
                        brand_name, model = car_name.split(' ', 1)  # Split on the first space
                        car = Car.objects.get(brand_name=brand_name, model=model)  # Fetch the car by brand and model
                        car.selled = True
                        car.save()
                    except (ValueError, Car.DoesNotExist) as e:
                        print(f"Error processing car {car_name}: {e}")
        else:
            print('User is not authenticated')  # Debug print
        
        if not last_customer_data:
            return JsonResponse({'error': 'Customer data not found.'}, status=404)
    
    except Exception as e:
       return JsonResponse({'error': str(e)}, status=500)

    context = {
       'last_customer_data': last_customer_data,
       "last_customer_data_details": {
            "name": last_customer_data.name,
            "email": last_customer_data.email,
            "mobile_phone": last_customer_data.mobile_phone,
            "cars": last_customer_data.cars,
            "deposit": last_customer_data.deposit,
            "downpayment": last_customer_data.downpayment,
            "monthly_installment": last_customer_data.monthly_installment,
            "total_amount": last_customer_data.total_amount,
            "bank": last_customer_data.bank,
            "passport": request.build_absolute_uri(last_customer_data.passport.url) if last_customer_data.passport else '',
            "driver_license": request.build_absolute_uri(last_customer_data.driver_license.url) if last_customer_data.driver_license else '',
            "personal_identification_card": request.build_absolute_uri(last_customer_data.personal_identification_card.url) if last_customer_data.personal_identification_card else '',
            "salary_certificate": request.build_absolute_uri(last_customer_data.salary_certificate.url) if last_customer_data.salary_certificate else '',
            "bank_statement": request.build_absolute_uri(last_customer_data.bank_statement.url) if last_customer_data.bank_statement else '',
            "pick_up_date": last_customer_data.pick_up_date,
            "pick_up_time": last_customer_data.pick_up_time,
            "pick_up_location": last_customer_data.pick_up_location,
        }
    }

    return render(request, 'installments_success_dp.html', context)

def installments_payment_success(request):
    '''Handle successful payments and updates customer data.'''
    try:
        # Update customer data
        if request.user.is_authenticated:
            last_customer_data = InstallmentsCustomerWithoutDP.objects.filter(user=request.user).order_by('-id').first()

            # Assuming `cars` field in `CustomersData` contains the brand and model names of the cars sold
            if last_customer_data and last_customer_data.cars:
                car_names = last_customer_data.cars.split(', ')  # Split the comma-separated string into a list of car names
                for car_name in car_names:
                    try:
                        # Split the car name into brand and model
                        brand_name, model = car_name.split(' ', 1)  # Split on the first space
                        car = Car.objects.get(brand_name=brand_name, model=model)  # Fetch the car by brand and model
                        car.selled = True
                        car.save()
                    except (ValueError, Car.DoesNotExist) as e:
                        print(f"Error processing car {car_name}: {e}")
        else:
            print('User is not authenticated')  # Debug print
        
        if not last_customer_data:
            return JsonResponse({'error': 'Customer data not found.'}, status=404)
    
    except Exception as e:
       return JsonResponse({'error': str(e)}, status=500)

    context = {
       'last_customer_data': last_customer_data,
       "last_customer_data_details": {
            "name": last_customer_data.name,
            "email": last_customer_data.email,
            "mobile_phone": last_customer_data.mobile_phone,
            "cars": last_customer_data.cars,
            "deposit": last_customer_data.deposit,
            "monthly_installment": last_customer_data.monthly_installment,
            "total_amount": last_customer_data.total_amount,
            "bank": last_customer_data.bank,
            "passport": request.build_absolute_uri(last_customer_data.passport.url) if last_customer_data.passport else '',
            "driver_license": request.build_absolute_uri(last_customer_data.driver_license.url) if last_customer_data.driver_license else '',
            "personal_identification_card": request.build_absolute_uri(last_customer_data.personal_identification_card.url) if last_customer_data.personal_identification_card else '',
            "salary_certificate": request.build_absolute_uri(last_customer_data.salary_certificate.url) if last_customer_data.salary_certificate else '',
            "bank_statement": request.build_absolute_uri(last_customer_data.bank_statement.url) if last_customer_data.bank_statement else '',
            "pick_up_date": last_customer_data.pick_up_date,
            "pick_up_time": last_customer_data.pick_up_time,
            "pick_up_location": last_customer_data.pick_up_location,
        }
    }

    return render(request, 'installments_success.html', context)




def cash_payment_cancel(request):
    '''Display cancel page if the cash payment failed''' 
    cart = None        
    cartitems = []

    if request.user.is_authenticated:
            cart , created = Cart.objects.get_or_create(user =request.user , completed = False)
            cartitems = cart.cartitems.all()
            
    # Calculate the total amount using total_price()
    total_amount = int(cart.total_price() * 100)  # Assuming total_price returns value in dollars

    try:
        stripe_total_price = total_amount # Use total_price() instead of price
    except:
        stripe_total_price = 0

    context = {
        'stripe_total_price': stripe_total_price,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'cash_cancel.html', context)

def deposit_payment_cancel(request):
    '''Display cancel page if the deposit payment failed'''
    # Calculate the total amount using total_price()
    deposit = int(3000 * 100)

    try:
        stripe_deposit = deposit
    except:
        stripe_deposit = 0

    context = {
        'stripe_deposit': stripe_deposit,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'deposit_cancel.html', context)

def remaining_payment_cancel(request):
    '''Display cancel page if the remaining payment failed'''
    # Calculate the total amount using total_price()
    last_customer_data = CustomersData.objects.filter(user=request.user).order_by('-id').first()
    remaining_price = last_customer_data.remaining_amount

    try:
        stripe_remaining = remaining_price
    except:
        stripe_remaining = 0

    context = {
        'stripe_remaining': stripe_remaining,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'remaining_cancel.html', context)

def installments_payment_cancel(request):
    '''Display cancel page if the deposit installments payment failed'''
    # Calculate the total amount using total_price()
    deposit = int(3000 * 100)

    try:
        stripe_deposit = deposit
    except:
        stripe_deposit = 0

    context = {
        'stripe_deposit': stripe_deposit,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'installments_cancel.html', context)





def sign_in(request):
    '''Sign in the website for new users'''
    if request.method =='POST':   
        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid(): 
            user = form.save()              
            #log the user in
            login(request , user)           
            return redirect('c7_motors:home')
    else:           
       form = forms.CustomUserCreationForm()     
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




def add_to_cart(request):
    '''Add Cars To Customer Shopping Cart'''
    data = json.loads(request.body)
    car_id = data["id"]
    car = Car.objects.get(id = car_id)

    if request.user.is_authenticated:
        cart , created = Cart.objects.get_or_create(user =request.user,completed = False)
        cartitems , created = CarsCart.objects.get_or_create(cart = cart,car = car)
        cartitems.save()

    return JsonResponse('Add Item Done' , safe=False)

def delete_item(request):
    '''Delete Cars From Customer Shopping Cart'''
    data = json.loads(request.body)
    car_id = data['id']
    item = Car.objects.get(id = car_id)
    if request.user.is_authenticated:
        cart = Cart.objects.get(user = request.user , completed = False)
        cart_items = CarsCart.objects.filter(cart=cart , car_id =car_id) 
        cart_items.delete()
    return JsonResponse('Delete Item Done' , safe= False)

def calculate_customer_salary(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)

    if request.method == 'POST':
        try:
            body = json.loads(request.body) if request.content_type == 'application/json' else request.POST

            salary = float(body.get('salary', 0))
            salary_bank = body.get('salary_bank', "")
            monthly_payments_bank = body.get('monthly_payments_bank', "")
            nationality = body.get('nationality', "")
            action = body.get('action', "")  # Determine which button was clicked

            # Handle cart and cart items
            cart, _ = Cart.objects.get_or_create(user=request.user, completed=False)
            cartitems = cart.cartitems.all()
            
            if not cartitems.exists():
                return JsonResponse({'error': 'No cars in cart'}, status=400)

            total_price = cart.total_price()
            downpayment = total_price * (0.2 if salary_bank == monthly_payments_bank else 0.3)
            monthly_without_dp = cartitems.first().car.monthly_installments_price
            annual_interest = ((total_price - downpayment) * (0.03 if nationality == "Emirati" else 0.038))

            total_with_dp = total_price + (annual_interest * 5)
            total_without_dp = monthly_without_dp * 60
            monthly_with_dp = ((total_price - downpayment) + (annual_interest * 5)) / 60

            car_names = [f"{item.car.brand_name} {item.car.model}" for item in cartitems]

            if action == "pay_deposit":
                # Update InstallmentsCustomer (with downpayment)
                customer, _ = InstallmentsCustomer.objects.get_or_create(user=request.user)
                customer.cars = ', '.join(car_names)
                customer.bank = monthly_payments_bank
                customer.downpayment = downpayment
                customer.monthly_installment = monthly_with_dp
                customer.total_amount = total_with_dp
                customer.save()

            elif action == "continue_without_dp":
                # Update InstallmentsCustomerWithoutDP (without downpayment)
                customer_without_dp, _ = InstallmentsCustomerWithoutDP.objects.get_or_create(user=request.user)
                customer_without_dp.cars = ', '.join(car_names)
                customer_without_dp.bank = monthly_payments_bank
                customer_without_dp.monthly_installment = monthly_without_dp
                customer_without_dp.total_amount = total_without_dp
                customer_without_dp.save()

            return JsonResponse({
                'downpayment': f"AED {downpayment:.2f}",
                'monthly_with_dp': f"AED {monthly_with_dp:.2f}",
                'monthly_without_dp': f"AED {monthly_without_dp:.2f}",
                'annual_interest': f"AED {annual_interest:.2f}",
                'total_with_dp': f"AED {total_with_dp:.2f}",
                'total_without_dp': f"AED {total_without_dp:.2f}",
                'cars': ', '.join(car_names)
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'GET':
        cart, _ = Cart.objects.get_or_create(user=request.user, completed=False)
        items = cart.cartitems.all()
        return render(request, "calculater.html", {"items": items})

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def add_data_GS(request):
    if request.method == 'POST':
        form = MayNumbersForm(request.POST)
        if form.is_valid():
            new_phone_number = form.save()
            try:
                write_sheet_data([new_phone_number.phone_number, str(new_phone_number.date)])
                return redirect('c7_motors:home')
            except Exception as e:
                return JsonResponse({'status': 'Failed to write to Google Sheet', 'error': str(e)})
        else:
            return JsonResponse({'status': 'Form is invalid', 'errors': form.errors})

    # GET request fallback
    form = MayNumbersForm()
    return render(request, 'home.html', {'form': form})