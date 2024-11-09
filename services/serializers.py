from rest_framework import serializers

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
    id_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    id_car= serializers.PrimaryKeyRelatedField(queryset=Car.objects.all(), write_only=True)
    id_workshop = serializers.PrimaryKeyRelatedField(queryset=Workshop.objects.all(), write_only=True)

    appointment_status = AppointmentStatusSerializer(read_only=True)

    user = UserRegisterSerializer(read_only=True)
    car = CarsSerializer(read_only=True)
    workshops = WorkshopSerializer(read_only=True)

    class Meta:
        model = Appointments
        fields = ['id_appointment',  'user', 'car', 'workshops','id_user', 'id_car', 'id_workshop', 'description',
                  'date', 'appointment_status']

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        appointment = Appointments.objects.create(
            user=validated_data["id_user"],
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
