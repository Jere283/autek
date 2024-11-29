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

    user = serializers.SerializerMethodField(read_only=True)
    car = serializers.SerializerMethodField(read_only=True)
    workshops = serializers.SerializerMethodField(read_only=True)
    appointment_status = serializers.SerializerMethodField(read_only=True)

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
        solicitud_enviada_status = AppointmentStatus.objects.get(name="Solicitud enviada")
        user = self.context['request'].user
        appointment = Appointments.objects.create(
            user=user,
            car=validated_data["id_car"],
            workshops=validated_data["id_workshop"],
            description=validated_data["description"],
            appointment_status=solicitud_enviada_status,
            date=validated_data["date"],
        )
        return appointment


class AppointmentStatusPatchSerializer(serializers.ModelSerializer):

    appointment_status = serializers.PrimaryKeyRelatedField(queryset=AppointmentStatus.objects.all(), write_only=True)
    appointment_status_name = serializers.CharField(source='appointment_status.name', read_only=True)

    def validate(self, data):
        current_status = self.instance.appointment_status
        new_status = data.get('appointment_status')

        if current_status == new_status:
            raise serializers.ValidationError("The new status must be different from the current status.")

        return data


    class Meta:
        model = Appointments
        fields = ['appointment_status', 'appointment_status_name']


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
