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
# Create your models here

class CustomersData(models.Model):
    name = models.TextField(max_length=300, default='', blank=True)
    email = models.TextField(max_length=300, default='', blank=True)
    mobile_phone = models.TextField(blank=True, default='')
    cars = models.TextField(default='', blank=True)  # plural here

    Salaried = 'Salaried'
    Self_Employed = 'Self-Employed'

    EMPLOYMENT_TYPE = [
        (Salaried, 'Salaried'),
        (Self_Employed, 'Self-Employed'),
    ]

    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE, blank=True)
    created_at = models.DateTimeField(auto_now_add=True , null=True)

    def __str__(self):
        return f"cars:{self.cars} - name:{self.name}"




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

    history = HistoricalRecords()

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
