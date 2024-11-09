from rest_framework import serializers
from .models import Service, AppointmentStatus, Appointments, WorkshopsService, AppointmentsServices


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id_service', 'name', 'description']


class AppointmentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentStatus
        fields = ['id_appointment_status', 'name']


class AppointmentsSerializer(serializers.ModelSerializer):
    id_user = serializers.StringRelatedField()
    id_car = serializers.StringRelatedField()
    id_workshops = serializers.StringRelatedField()
    appointment_status = AppointmentStatusSerializer(read_only=True)

    class Meta:
        model = Appointments
        fields = ['id_appointment', 'id_user', 'id_car', 'id_workshops', 'description', 'date', 'appointment_status']


class WorkshopsServiceSerializer(serializers.ModelSerializer):
    workshop = serializers.StringRelatedField()
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = WorkshopsService
        fields = ['id_workshop_service', 'workshop', 'service', 'price']


class AppointmentsServicesSerializer(serializers.ModelSerializer):
    appointment = AppointmentsSerializer(read_only=True)
    service = WorkshopsServiceSerializer(read_only=True)

    class Meta:
        model = AppointmentsServices
        fields = ['id_appointment_service', 'appointment', 'service']
