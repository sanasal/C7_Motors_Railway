from django.contrib import admin
from django.contrib import messages
from .models import *

class CarAdmin(admin.ModelAdmin):
    list_display = ("brand_name", "model")

class CarImageZipAdmin(admin.ModelAdmin):
    list_display = ["car", "zip_file"]

    def save_model(self, request, obj, form, change):
        """Save model and notify user that extraction happens asynchronously."""
        super().save_model(request, obj, form, change)
        messages.success(request, "ZIP file uploaded. Images will be extracted soon.")

#Register Models
admin.site.register(Car, CarAdmin)
admin.site.register(CarImageZip, CarImageZipAdmin)
admin.site.register(Cart)
admin.site.register(customers_data)
admin.site.register(CarImages)
admin.site.register(CarsCart)
admin.site.register(InstallmentsCustomer)
admin.site.register(InstallmentsCustomerWithoutDP)