from django.contrib import admin
from django.contrib import messages
import os
from django.core.files import File
from django.conf import settings
from .models import Car, CarImages, Cart, customers_data, CarsCart, InstallmentsCustomer, InstallmentsCustomerWithoutDP

class CarImagesInline(admin.TabularInline):
    model = CarImages
    extra = 1  # Number of empty forms for adding images

class CarAdmin(admin.ModelAdmin):
    inlines = [CarImagesInline]
    list_display = ('brand_name', 'model', 'type', 'transmission', 'selled')
    list_filter = ('type', 'transmission', 'selled')
    search_fields = ('brand_name', 'model', 'exterior_color', 'interior_color')

    actions = ['import_photos_from_folder']

    def import_photos_from_folder(self, request, queryset):
        """
        Bulk import images from a folder into selected cars.
        """
        folder_path = os.path.join(settings.MEDIA_ROOT, "C7_Motors/media")  # Use original upload path

        if not os.path.exists(folder_path):
            self.message_user(request, "Folder does not exist!", level=messages.ERROR)
            return

        for car in queryset:
            images_added = 0
            for filename in os.listdir(folder_path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    file_path = os.path.join(folder_path, filename)

                    with open(file_path, 'rb') as f:
                        image = CarImages(product=car)  # Use 'product' instead of 'car'
                        image.image.save(filename, File(f), save=True)
                        images_added += 1

            self.message_user(request, f"Added {images_added} images to {car.brand_name} {car.model}", level=messages.SUCCESS)

    import_photos_from_folder.short_description = "Import photos from C7_Motors/media"

admin.site.register(Car, CarAdmin)
admin.site.register(Cart)
admin.site.register(customers_data)
admin.site.register(CarsCart)
admin.site.register(CarImages)
admin.site.register(InstallmentsCustomer)
admin.site.register(InstallmentsCustomerWithoutDP)