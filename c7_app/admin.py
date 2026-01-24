from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.models import User, Group
from .models import *
from django.urls import path
from django.shortcuts import render
from simple_history.admin import SimpleHistoryAdmin

class CustomAdminSite(admin.AdminSite):
    site_header = "C7 Motors Administration"
    site_title = "Admin Site"
    site_index_title = "C7 Motors"

    def get_app_list(self, request , app_label = 'C7 Motors'):
        """Customize the display of models in the Django admin index page."""
        app_list = super().get_app_list(request)

        # Define sections
        car_details_section = {"name": "Cars Data","app_label":"Cars", "models": []}
        customers_section = {"name": "Customers Data","app_label":"Customers", "models": []}
        auth_section = {"name": "Authentication and Authorization","app_label":"Authentication and Authorization", "models": []}

        # Iterate over apps and categorize models
        for app in app_list:
            for model in app["models"]:
                if model["object_name"] in ["CarImageZip", "CarImage", "Car" , "ExtraFeature" , "TechnicalFeature"]:
                    car_details_section["models"].append(model)

                elif model["object_name"] in ["User", "CustomUser" , "Group"]:
                    auth_section["models"].append(model)

                else:
                    customers_section["models"].append(model)

        return [auth_section,car_details_section, customers_section]

@admin.action(description="Mark as Selled")
def mark_as_selled(modeladmin ,requset ,queryset):
    queryset.update(selled = True)

@admin.action(description="Mark as Not Available")
def mark_as_not_available(modeladmin , request , queryset):
    queryset.update(not_available = True)

class CarImagesInline(admin.TabularInline):
    model = CarImage

class TechnicalFeatureAdmin(admin.ModelAdmin):
    search_fields = ("name",)

class ExtraFeatureAdmin(admin.ModelAdmin):
    search_fields = ("name",)

class CarAdmin(SimpleHistoryAdmin , admin.ModelAdmin):
    list_display = ["brand_name", "model", "selled" , "not_available"]
    filter_horizontal = ("technical_features","extra_features")
    search_fields = ["brand_name" , "model" , "model_year"]
    list_filter = ["brand_name" ,  "model" , "model_year"]
    inlines = [CarImagesInline]
    actions = [mark_as_selled , mark_as_not_available]

class CarImagesAdmin(admin.ModelAdmin):
    list_per_page = 30

class CarImageZipAdmin(admin.ModelAdmin):
    list_display = ["car", "zip_file"]

    def save_model(self, request, obj, form, change):
        """Save model and notify user that extraction happens asynchronously."""
        super().save_model(request, obj, form, change)
        messages.success(request, "ZIP file uploaded. Images will be extracted soon.")


# Register the custom admin site
custom_admin_site = CustomAdminSite(name="custom_admin")

# Register models under the new admin site
custom_admin_site.register(CarImageZip , CarImageZipAdmin)
custom_admin_site.register(CarImage , CarImagesAdmin)
custom_admin_site.register(Car , CarAdmin)
custom_admin_site.register(Group)
custom_admin_site.register(RequestsData)
custom_admin_site.register(User)
custom_admin_site.register(Article)
custom_admin_site.register(TechnicalFeature)
custom_admin_site.register(ExtraFeature)