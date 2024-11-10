from rest_framework import serializers, viewsets

from cars.models import Car
from cars.serializers import CarsSerializer
from users.models import User
from users.serializers import UserRegisterSerializer
from workshops.models import Workshop
from workshops.serializers import WorkshopSerializer
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
    id_car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all(), write_only=True)
    id_workshop = serializers.PrimaryKeyRelatedField(queryset=Workshop.objects.all(), write_only=True)

    # Use SerializerMethodField for detailed fields
    user = serializers.SerializerMethodField()
    car = serializers.SerializerMethodField()
    workshops = serializers.SerializerMethodField()
    appointment_status = serializers.SerializerMethodField()

    class Meta:
        model = Appointments
        fields = ['id_appointment', 'user', 'car', 'workshops', 'id_car', 'id_workshop',
                  'description', 'date', 'appointment_status']

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "first_name": obj.user.first_name,
            "email": obj.user.email
        }

    def get_car(self, obj):
        return {
            "id": obj.car.id_car,
            "brand": obj.car.brand.name,
            "model": obj.car.model.name,
            "license_plate": obj.car.license_plate
        }

    def get_workshops(self, obj):
        return {
            "id": obj.workshops.id_workshop,
            "name": obj.workshops.name,
        }

    def get_appointment_status(self, obj):
        if obj.appointment_status:
            return {
                "id": obj.appointment_status.id_appointment_status,
                "name": obj.appointment_status.name
            }
        return None

    def create(self, validated_data):
        user = self.context['request'].user
        appointment = Appointments.objects.create(
            user=user,
            car=validated_data["id_car"],
            workshops=validated_data["id_workshop"],
            description=validated_data["description"],
            date=validated_data["date"],
        )
        return appointment


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
