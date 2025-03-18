#models.py
from django.db import models
from xml.parsers.expat import model
from django.db import models
from django.contrib.auth.models import User
import uuid
import os
import zipfile
from django.core.files.base import ContentFile

# Create your models here

class customers_data(models.Model):
    user = models.ForeignKey(User,null = True, on_delete = models.SET_NULL) 
    cars = models.TextField(default='', blank=True)
    name = models.TextField(max_length=300, default='', blank=True)
    email = models.TextField(max_length=300, default='', blank=True)
    mobile_phone = models.TextField(blank=True, default='')
    total_amount =models.IntegerField(null=True)
    paid_amount = models.IntegerField(null=True)
    remaining_amount = models.IntegerField(null=True , default='')
    pick_up_location = models.TextField(max_length=300, default='', blank=True)
    pick_up_date = models.DateField(null=True, blank=True)
    pick_up_time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True , null=True)

    def save(self, *args, **kwargs):
        # Automatically calculate the remaining amount
        if self.total_amount is not None and self.paid_amount is not None:
            self.remaining_amount = self.total_amount - self.paid_amount
        super(customers_data, self).save(*args, **kwargs)

    def __str__(self):
        return f"cars:{self.cars} - user:{self.user} - name:{self.name}"


class InstallmentsCustomer(models.Model):
    user = models.ForeignKey(User,null = True, on_delete = models.SET_NULL) 
    cars = models.TextField(default='', blank=True)
    name = models.TextField(max_length=300, default='', blank=True)
    email = models.TextField(max_length=300, default='', blank=True)
    mobile_phone = models.TextField(blank=True, default='')
    deposit = 3000
    downpayment = models.IntegerField(null=True)
    monthly_installment = models.IntegerField(null=True)
    total_amount = models.IntegerField(null=True)
    bank = models.TextField(max_length=300, default='', blank=True)
    passport = models.FileField(default = '' , blank=True)
    driver_license = models.FileField(default = '' , blank=True)
    personal_identification_card = models.FileField(default = '' , blank=True)
    salary_certificate = models.FileField(default = '' , blank=True)
    bank_statement = models.FileField(default = '' , blank=True)
    pick_up_location = models.TextField(max_length=300, default='', blank=True)
    pick_up_date = models.DateField(null=True, blank=True)
    pick_up_time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True , null=True)

    def __str__(self):
        return f"cars:{self.cars} - user:{self.user} - name:{self.name}"

class InstallmentsCustomerWithoutDP(models.Model):
    user = models.ForeignKey(User,null = True, on_delete = models.SET_NULL) 
    cars = models.TextField(default='', blank=True)
    name = models.TextField(max_length=300, default='', blank=True)
    email = models.TextField(max_length=300, default='', blank=True)
    mobile_phone = models.TextField(blank=True, default='')
    deposit = 3000
    monthly_installment = models.IntegerField(null=True)
    total_amount = models.IntegerField(null=True)
    bank = models.TextField(max_length=300, default='', blank=True)
    passport = models.FileField(default = '' , blank=True)
    driver_license = models.FileField(default = '' , blank=True)
    personal_identification_card = models.FileField(default = '' , blank=True)
    salary_certificate = models.FileField(default = '' , blank=True)
    bank_statement = models.FileField(default = '' , blank=True)
    pick_up_location = models.TextField(max_length=300, default='', blank=True)
    pick_up_date = models.DateField(null=True, blank=True)
    pick_up_time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True , null=True)

    def __str__(self):
        return f"cars:{self.cars} - user:{self.user} - name:{self.name}"


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4 , primary_key=True)
    user = models.ForeignKey(User,null = True, on_delete = models.SET_NULL) 
    completed =  models.BooleanField(default=False)

    def total_price(self):

        cartitems = self.cartitems.all()

        cars_total = sum ([item.cars_cash_price() for item in cartitems])

        total_price_without_discount =  cars_total

        total_dicount = 0

        discount = 0

        total_price_after_discount = total_price_without_discount - (total_price_without_discount * discount)

        return int(total_price_after_discount)

    def __str__(self):
       return f"{self.id} - {self.user}"


class Car(models.Model):
    brand_name = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    main_img = models.ImageField(default='', blank=True)

    SUV = 'SUV'
    SEDAN = 'Sedan'
    HATCHBACK = 'Hatchback'
    HYBRID = 'Hybrid'
    ELECTRIC = 'Electric'
    COUPE = 'Coupe'
    
    TYPE_CHOICES = [
        (SUV, 'SUV'),
        (SEDAN, 'Sedan'),
        (HATCHBACK, 'Hatchback'),
        (HYBRID, 'Hybrid'),
        (ELECTRIC, 'Electric'),
        (COUPE, 'Coupe'),
    ]

    type = models.CharField(max_length=20, choices=TYPE_CHOICES, blank=True)
    exterior_color = models.CharField(max_length=100, blank=True)
    interior_color = models.CharField(max_length=100, blank=True)
    
    MANUAL = 'Manual'
    AUTOMATIC = 'Automatic'
    GEAR_CHOICES = [
        (MANUAL, 'Manual Transmission'),
        (AUTOMATIC, 'Automatic Transmission'),
    ]
    
    transmission = models.CharField(max_length=20, choices=GEAR_CHOICES)
    model_year = models.IntegerField(null=True, blank=True)
    mileage = models.IntegerField(null=True, blank=True)
    cash_price = models.IntegerField(null=True, blank=True)
    monthly_installments_price = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    selled = models.BooleanField(default=False)

    def delete_selled_car_images(self):
        """Delete all images from storage and database when a car is sold."""
        if self.selled:
            for img in self.images.all():  
                if img.image and os.path.exists(img.image.path):  
                    os.remove(img.image.path) 
                img.delete()  

    def save(self, *args, **kwargs):
        """Override save to check when a car is marked as sold."""
        if self.pk:
            old_car = Car.objects.filter(pk=self.pk).first()
            if old_car and not old_car.selled and self.selled:
                self.delete_selled_car_images()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand_name} {self.model}"

class CarImages(models.Model):
    car = models.ForeignKey(Car, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="car_images/" , null=True)

    def __str__(self):
        return f"{self.car.brand_name} {self.car.model}"


class CarImageZip(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    zip_file = models.FileField(upload_to="car_images/")

    def extract_images(self):
        """Extract images from the uploaded ZIP file and save them in CarImages."""
        if not self.zip_file or not self.zip_file.name:
            print("No ZIP file provided.")
            return

        zip_path = self.zip_file.path
        print(f"Extracting from ZIP path: {zip_path}")

        # Ensure file exists before attempting extraction
        if not os.path.exists(zip_path):
            print(f"Error: ZIP file not found at {zip_path}")
            return

        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                for filename in zip_ref.namelist():
                    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                        with zip_ref.open(filename) as img_file:
                            img_data = img_file.read()
                            new_image = CarImages(car=self.car)
                            new_image.image.save(filename, ContentFile(img_data))
                            new_image.save()
                            print(f"Saved image: {filename}")

        except zipfile.BadZipFile:
            print("Error: Invalid ZIP file format.")
        except Exception as e:
            print(f"Unexpected error: {e}")


class CarsCart(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE , related_name='items')
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE , related_name='cartitems')

    def __str__(self):
        return f"{self.car.brand_name} - ${self.car.cash_price} - {self.cart.user}"

    def cars_cash_price(self):
        car_price = int(self.car.cash_price)
        cars_total_price = car_price
        return cars_total_price