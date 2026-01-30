from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from c7_app.models import *

# صفحات ثابتة
class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return [
            'c7_motors:about',
            'c7_motors:contact_us',
            'c7_motors:financing',
        ]

    def location(self, item):
        return reverse(item)

# صفحات ديناميكية
class HomeSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Car.objects.only('id', 'cash_price', 'main_img', 'brand_name', 'model','model_year', 'mileage', 'selled', 'not_available')[40:]

    def location(self, obj):
        return reverse('c7_motors:home')
    

class InventorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Car.objects.all().only('id', 'cash_price', 'main_img', 'brand_name', 'model','model_year', 'mileage', 'selled', 'not_available').order_by('-id')

    def location(self, obj):
        return reverse('c7_motors:inventory')
        
        
        
class ArticlesSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Article.objects.all()

    def location(self, obj):
        return reverse('c7_motors:articles')