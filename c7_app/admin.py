from django.contrib import admin
from .models import  Car,Cart , customers_data , CarsCart , CarImages , InstallmentsCustomer , InstallmentsCustomerWithoutDP

# Register your models here.
class CarImagesInline(admin.TabularInline):  # Or use StackedInline
    model = CarImages
    extra = 1  # Number of empty forms to display for adding images
    fields = ['image']  # Only show the `image` field for editing

class CarAdmin(admin.ModelAdmin):
    inlines = [CarImagesInline]

admin.site.register(Car, CarAdmin)
admin.site.register(Cart)
admin.site.register(customers_data)
admin.site.register(CarsCart)
admin.site.register(CarImages)
admin.site.register(InstallmentsCustomer)
admin.site.register(InstallmentsCustomerWithoutDP)