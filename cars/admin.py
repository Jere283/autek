from django.contrib import admin
from .models import CarModels, Cars, Colors, CarBrands

# Register your models here.

admin.site.register(Cars)
admin.site.register(Colors)
admin.site.register(CarBrands)
admin.site.register(CarModels)