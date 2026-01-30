# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.cache import cache_page
from django.utils import translation
from django.views.decorators.http import require_http_methods
from django.db.models import Prefetch
import json, urllib

from .models import Car, Article
from .forms import RequestsForm
from c7_motors import deployment

def switch_language(request, lang_code):
    translation.activate(lang_code)
    request.session['django_language'] = lang_code

    response = redirect(request.META.get('HTTP_REFERER', '/'))
    response.set_cookie(deployment.LANGUAGE_COOKIE_NAME, lang_code)
    return response

def home(request):
    cars = (
        Car.objects
        .filter(selled=False, not_available=False)
        .only(
            'id', 'cash_price', 'main_img', 'brand_name',
            'model', 'model_year', 'mileage'
        )
        .order_by('-id')[:15]
    )

    articles = Article.objects.only('id', 'title', 'image')[:4]

    context = {
        'cars': cars,
        'articles': articles,
        'models_years': Car.objects.values_list(
            'model_year', flat=True
        ).distinct().order_by('model_year'),
        'cars_brands': Car.objects.values_list(
            'brand_name', flat=True
        ).distinct().order_by('brand_name'),
    }
    return render(request, 'home.html', context)




def inventory(request):
    cars = (
        Car.objects
        .only(
            'id', 'cash_price', 'main_img', 'brand_name',
            'model', 'model_year', 'mileage'
        )
        .order_by('-id')
    )
    return render(request, 'inventory.html', {'cars': cars})



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


@require_http_methods(["GET", "POST"])
def financing(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            car_price = float(data.get('car_price', 0))
            downpayment = float(data.get('downpayment', 0))
            loan_duration = int(data.get('loan_duration', 1))

            interest = (car_price * 0.04) / 12
            total = car_price + (interest * loan_duration)
            monthly = (total - downpayment) / loan_duration

            return JsonResponse({
                'estimated_monthly_payment': f"AED {monthly:.2f}"
            })

        except Exception:
            return JsonResponse({'error': 'Invalid data'}, status=400)

    return render(
        request,
        "financing.html",
        {
            'cars': Car.objects.only('id', 'brand_name', 'model'),
            'form': RequestsForm()
        }
    )



def get_it_now(request , car_id):
    '''Get It Now Request'''

    car = Car.objects.get(id=car_id)

    context = {'car':car}

    return render(request , 'get_it_now.html' , context)



def _handle_request_form(request, template):
    form = RequestsForm(request.POST)
    if not form.is_valid():
        return render(request, template, {'form': form})

    data = form.save()

    message = urllib.parse.quote(
        f"Car: {data.car}\n"
        f"Name: {data.name}\n"
        f"Phone: {data.mobile_phone}\n"
        f"Payment: {data.payment_method}\n"
        f"Lang: {data.language}"
    )

    return redirect(f"https://wa.me/971562341000?text={message}")

@require_http_methods(["POST"])
def add_financing_request_data(request):
    return _handle_request_form(request, 'financing.html')

@require_http_methods(["POST"])
def add_request_data(request):
    return _handle_request_form(request, 'get_it_now.html')


@cache_page(60 * 10)  # 10 minutes cache
def cars(request, car_type=None):
    """
    High-performance cars listing with optional type filtering
    """

    cars = (
        Car.objects
        .filter(selled=False, not_available=False)
        .only(
            'id',
            'brand_name',
            'model',
            'model_year',
            'cash_price',
            'main_img',
            'mileage'
        )
        .order_by('-id')
    )

    if car_type:
        cars = cars.filter(type=car_type)

    context = {
        'cars': cars,
        'car_type': car_type
    }

    return render(request, 'cars.html', context)

def cars_search(request):
    cars = Car.objects.all()

    filters = {
        'model_year': request.GET.get('year'),
        'type': request.GET.get('style'),
    }

    for field, value in filters.items():
        if value:
            cars = cars.filter(**{field: value})

    if brand := request.GET.get('brand'):
        cars = cars.filter(brand_name__icontains=brand)

    if request.GET.get('price_from') and request.GET.get('price_to'):
        cars = cars.filter(
            cash_price__range=(
                request.GET['price_from'],
                request.GET['price_to']
            )
        )

    return render(request, 'cars.html', {'cars': cars})


def car_details(request, car_slug):
    car = get_object_or_404(
        Car.objects.prefetch_related(
            'images',
            'technical_features',
            'driver_assistance_and_safty',
            'comfort_and_convenience',
            'exterior'
        ),
        slug=car_slug
    )

    context = {
        'car': car,
        'description_lines': car.description.splitlines(),
        'car_images': car.images.all(),
        'technical_features': car.technical_features.all(),
        'driver_assistance_and_safty': car.driver_assistance_and_safty.all(),
        'comfort_and_convenience': car.comfort_and_convenience.all(),
        'exterior': car.exterior.all(),
    }

    return render(request, 'car_details.html', context)