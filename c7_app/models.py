#models.py
from django.db import models
from xml.parsers.expat import model
from django.db import models
from django.contrib.auth.models import User
import uuid
import os
import zipfile
from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from simple_history.models import HistoricalRecords
from django.utils.text import slugify
# Create your models here

class TechnicalFeature(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    

class ExtraFeature(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Car(models.Model):
    brand_name = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(unique=True,max_length=200,blank=True,null=True)
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
    specification = models.CharField(max_length=40 , null=True)
    horsepower = models.PositiveIntegerField(null=True, blank=True)
    engine_capacity = models.PositiveIntegerField(null=True, blank=True)
    cylinders = models.PositiveIntegerField(null=True, blank=True)
    seating_capacity = models.PositiveIntegerField(null=True, blank=True)
    monthly_installments_price = models.IntegerField(null=True, blank=True)
    technical_features = models.ManyToManyField(TechnicalFeature, blank=True)
    extra_features = models.ManyToManyField(ExtraFeature, blank=True)
    description = models.TextField(blank=True)
    selled = models.BooleanField(default=False)
    not_available = models.BooleanField(default=False)

    history = HistoricalRecords()

    def delete_selled_car_images(self):
        """Delete all images from storage and database when a car is sold."""
        if self.selled or self.not_available:
            for img in self.images.all():  
                if img.image and os.path.exists(img.image.path):  
                    os.remove(img.image.path) 
                img.delete()  

    def save(self, *args, **kwargs):
        if not self.slug and self.brand_name:
            base_slug = slugify(f"{self.brand_name} {self.model}")
            slug = base_slug
            counter = 1
    
            while Car.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
    
            self.slug = slug
    
        # handle sold cars
        if self.pk:
            old_car = Car.objects.filter(pk=self.pk).first()
            if old_car and not old_car.selled and self.selled:
                self.delete_selled_car_images()
    
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand_name} {self.model}"

class CarImage(models.Model):
    car = models.ForeignKey(Car, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="car_images/" , null=True)

    def __str__(self):
        return f"{self.car.brand_name} {self.car.model}"


class CarImageZip(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE , related_name="zip_files")
    zip_file = models.FileField(upload_to="car_zips/" , null=True)

    def extract_images(self):
        """Extract images from the uploaded ZIP file."""
        if self.zip_file:
            zip_path = self.zip_file.path

            if not os.path.exists(zip_path):
                print(f"ZIP file does NOT exist: {zip_path}")
                return

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                for filename in zip_ref.namelist():
                    if filename.endswith((".jpg", ".jpeg", ".png")):
                        img_data = zip_ref.read(filename)
                        new_image = CarImage(car=self.car)
                        new_image.image.save(filename, ContentFile(img_data))
                        new_image.save()

@receiver(post_save, sender=CarImageZip)
def extract_images_after_save(sender, instance, created, **kwargs):
    """Extract images only after the ZIP file is fully saved."""
    if created:  # Only on first save, to prevent loops
        instance.extract_images()



class Article(models.Model):
    user = models.ForeignKey(User,null = True, on_delete = models.SET_NULL) 
    image = models.ImageField(default='', blank=True)
    type = models.CharField(blank=True , max_length=100)
    title = models.CharField(blank=True , max_length=300)
    header = models.TextField(blank=True)
    read_more = models.TextField(blank=True)
    
class RequestsData(models.Model):
    car = models.TextField(default='', blank=True) 
    name = models.TextField(max_length=300, default='', blank=True)
    mobile_phone = models.TextField(blank=True, default='')
    Cash = 'Cash'
    Bank_Financing = 'Bank-Financing'

    PAYMENT_METHODS = [
        (Cash, 'Cash'),
        (Bank_Financing, 'Bank-Financing'),
    ]

    Arabic = 'Arabic'
    English = 'English'

    LANGUAGE = [
        (Arabic , 'Arabic'),
        (English , 'English')
    ]

    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, blank=True)
    language = models.CharField(max_length=20 , choices=LANGUAGE , blank=True)
    created_at = models.DateTimeField(auto_now_add=True , null=True)

    def __str__(self):
        return f"cars:{self.car} - name:{self.name}"