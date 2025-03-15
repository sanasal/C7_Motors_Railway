from django.contrib import admin
from django.contrib import messages
import os
from django.core.files import File
from django.conf import settings
from django.utils.html import format_html
from django.shortcuts import redirect
from django.urls import path
from django.http import HttpResponseRedirect
from .models import Car, CarImages, Cart, customers_data, CarsCart, InstallmentsCustomer, InstallmentsCustomerWithoutDP

class CarImagesInline(admin.TabularInline):
    model = CarImages
    extra = 1  # Allows adding one more inline image manually

class CarAdmin(admin.ModelAdmin):
    inlines = [CarImagesInline]
    list_display = ('brand_name', 'model', 'type', 'transmission', 'selled')
    list_filter = ('type', 'transmission', 'selled')
    search_fields = ('brand_name', 'model', 'exterior_color', 'interior_color')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-images/<int:car_id>/', self.admin_site.admin_view(self.import_images_view), name='import_car_images'),
        ]
        return custom_urls + urls

    def import_images_view(self, request, car_id):
        car = Car.objects.get(id=car_id)
        folder_path = os.path.join(settings.MEDIA_ROOT, "C7_Motors/media")  # Change this to your actual folder

        if not os.path.exists(folder_path):
            messages.error(request, "Folder does not exist!")
            return redirect(request.META.get('HTTP_REFERER', 'admin:index'))

        images_added = 0
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                file_path = os.path.join(folder_path, filename)

                with open(file_path, 'rb') as f:
                    image = CarImages(product=car)  # Use 'product' as per your model
                    image.image.save(filename, File(f), save=True)
                    images_added += 1

        messages.success(request, f"Added {images_added} images to {car.brand_name} {car.model}")
        return redirect(request.META.get('HTTP_REFERER', 'admin:index'))


        def import_images_button(self, obj):
            if obj and obj.pk:  # Ensure the car is saved before showing the button
                return format_html('<a href="{}" class="button" style="padding: 6px 12px; background: #007bff; color: white; border-radius: 5px; text-decoration: none;">Import Images</a>', f"/admin/import-images/{obj.id}/")
            return format_html('<span style="color: red;">Save this car first!</span>')



    import_images_button.short_description = "Import Images"
    import_images_button.allow_tags = True

    readonly_fields = ['import_images_button']

admin.site.register(Car, CarAdmin)
admin.site.register(Cart)
admin.site.register(customers_data)
admin.site.register(CarsCart)
admin.site.register(CarImages)
admin.site.register(InstallmentsCustomer)
admin.site.register(InstallmentsCustomerWithoutDP)
