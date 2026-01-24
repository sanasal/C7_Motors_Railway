from django.core.management.base import BaseCommand
from django.utils.text import slugify
from c7_app.models import Car

class Command(BaseCommand):
    help = "Generate slugs for cars without slugs"

    def handle(self, *args, **kwargs):
        cars = Car.objects.filter(slug__isnull=True) | Car.objects.filter(slug="")
        for car in cars:
            base_slug = slugify(car.name)
            slug = base_slug
            counter = 1
            
            while Car.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            car.slug = slug
            car.save()

        self.stdout.write(self.style.SUCCESS("Slugs generated successfully!"))
