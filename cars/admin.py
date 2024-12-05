from django.contrib import admin
from .models import CarModel, Car, Color, CarBrand

# Register your models here.

admin.site.register(Car)
admin.site.register(Color)
admin.site.register(CarBrand)
admin.site.register(CarModel)