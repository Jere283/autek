
from django.contrib import admin
from .models import Country, State, City, Address, Workshop


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id_country', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('id_state', 'name', 'country')
    search_fields = ('name',)
    list_filter = ('country',)
    ordering = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id_city', 'name', 'state')
    search_fields = ('name',)
    list_filter = ('state',)
    ordering = ('name',)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id_address', 'city', 'address')
    search_fields = ('address',)
    list_filter = ('city',)
    ordering = ('address',)


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('id_workshop', 'name', 'phone_number', 'email', 'address')
    search_fields = ('name', 'email')
    list_filter = ('address',)
    ordering = ('name',)
