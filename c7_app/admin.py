from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.models import User, Group
from .models import *

class CustomAdminSite(admin.AdminSite):
    site_header = "C7 Motors Administration"
    site_title = "Admin Site"
    index_title = "C7 Motors"

    def get_app_list(self, request):
        """Customize the display of models in the Django admin index page."""
        app_list = super().get_app_list(request)

        # Define sections
        car_details_section = {"name": "Cars Data", "app_label": "cars", "models": []}
        customers_section = {"name": "Customers Data", "app_label": "customers", "models": []}
        auth_section = {"name": "Authentication and Authorization", "app_label": "auth", "models": []}

        # Iterate over apps and categorize models
        for app in app_list:
            for model in app["models"]:
                if model["object_name"] in ["CarImageZip", "CarImages", "Car"]:
                    car_details_section["models"].append(model)

                elif model["object_name"] in ["User", "Group"]:
                    auth_section["models"].append(model)

                else:
                    customers_section["models"].append(model)

        return [auth_section,car_details_section, customers_section]

# Register the custom admin site
custom_admin_site = CustomAdminSite(name="custom_admin")

class CarImagesInline(admin.TabularInline):
    model = CarImages

class CarAdmin(admin.ModelAdmin):
    list_display = ["brand_name", "model"]
    search_fields = ["brand_name" , "model" , "model_year"]
    list_filter = ["brand_name" ,  "model" , "model_year"]

    inlines = [CarImagesInline]

class CarImageZipAdmin(admin.ModelAdmin):
    list_display = ["car", "zip_file"]

    def save_model(self, request, obj, form, change):
        """Save model and notify user that extraction happens asynchronously."""
        super().save_model(request, obj, form, change)
        messages.success(request, "ZIP file uploaded. Images will be extracted soon.")

# Register models under the new admin site
custom_admin_site.register(CarImageZip , CarImageZipAdmin)
custom_admin_site.register(CarImages)
custom_admin_site.register(Car , CarAdmin)
custom_admin_site.register(CarsCart)
custom_admin_site.register(InstallmentsCustomer)
custom_admin_site.register(InstallmentsCustomerWithoutDP)
custom_admin_site.register(Cart)
custom_admin_site.register(customers_data)
custom_admin_site.register(Group)
custom_admin_site.register(User)