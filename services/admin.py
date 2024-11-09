from django.contrib import admin
from .models import Service, AppointmentStatus, Appointments, WorkshopsService, AppointmentsServices


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id_service', 'name', 'description')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(AppointmentStatus)
class AppointmentStatusAdmin(admin.ModelAdmin):
    list_display = ('id_appointment_status', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Appointments)
class AppointmentsAdmin(admin.ModelAdmin):
    list_display = ('id_appointment', 'id_user', 'id_car', 'id_workshops', 'date', 'appointment_status')
    search_fields = ('id_user__username', 'id_car__license_plate')
    list_filter = ('appointment_status', 'date')
    ordering = ('date',)


@admin.register(WorkshopsService)
class WorkshopsServiceAdmin(admin.ModelAdmin):
    list_display = ('id_workshop_service', 'workshop', 'service', 'price')
    search_fields = ('workshop__name', 'service__name')
    ordering = ('workshop',)


@admin.register(AppointmentsServices)
class AppointmentsServicesAdmin(admin.ModelAdmin):
    list_display = ('id_appointment_service', 'appointment', 'service')
    search_fields = ('appointment__id_appointment', 'service__service__name')
