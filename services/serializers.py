from datetime import datetime

from rest_framework import serializers, viewsets
from cars.models import Car
from workshops.models import Workshop
from .models import Service, AppointmentStatus, Appointments, WorkshopsService, AppointmentsServices, \
    AppointmentsImages, Budgets, BudgetsStatus


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id_service', 'name', 'description']


class AppointmentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentStatus
        fields = ['id_appointment_status', 'name']


class AppointmentsImagesSerializer(serializers.ModelSerializer):
    id_appointment = serializers.PrimaryKeyRelatedField(
        queryset=Appointments.objects.all(),
        required=True,
        help_text="The ID of the related appointment."
    )

    class Meta:
        model = AppointmentsImages
        fields = ['id_image', 'id_appointment', 'url', 'description', 'created_at']
        read_only_fields = ['id_image', 'created_at']

    def create(self, validated_data):
        id_appointment = validated_data.get('id_appointment')
        url = validated_data.get('url')
        description = validated_data.get('description', None)
        created_at = datetime.now()


        if not id_appointment:
            raise serializers.ValidationError({"id_appointment": "Appointment ID is required."})

        return AppointmentsImages.objects.create(
            id_appointment=id_appointment,
            url=url,
            description=description,
            created_at=created_at
        )



class AppointmentsSerializer(serializers.ModelSerializer):
    id_car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all(), write_only=True)
    id_workshop = serializers.PrimaryKeyRelatedField(queryset=Workshop.objects.all(), write_only=True)

    user = serializers.SerializerMethodField(read_only=True)
    car = serializers.SerializerMethodField(read_only=True)
    workshops = serializers.SerializerMethodField(read_only=True)
    appointment_status = serializers.SerializerMethodField(read_only=True)
    images = AppointmentsImagesSerializer(many=True, read_only=True,source='appointmentsimages_set')


    class Meta:
        model = Appointments
        fields = ['id_appointment', 'user', 'car', 'workshops', 'id_car', 'id_workshop',
                  'description', 'date', 'appointment_status', 'images', 'approved_budget']
        read_only_fields =['approved_budget', 'appointment_status']

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
            "license_plate": obj.car.license_plate,
            "year": obj.car.year
        }

    def get_workshops(self, obj):
        return {
            "id": obj.workshops.id_workshop,
            "name": obj.workshops.name,
            "address": obj.workshops.address.address,
            "city": obj.workshops.address.city.name
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
    workshop_id = serializers.PrimaryKeyRelatedField(queryset=Workshop.objects.all(), write_only=True)
    service_id = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), write_only=True)

    workshop = serializers.SerializerMethodField(read_only=True)
    service = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = WorkshopsService
        fields = ['id_workshop_service', 'workshop', 'workshop_id', 'service','service_id', 'price']

    def get_workshop(self, obj):
        return {
            "id": obj.workshop.id_workshop,
            "name": obj.workshop.name,
            "address": obj.workshop.address.address,
            "city": obj.workshop.address.city.name
        }

    def get_service(self, obj):
        return {
            "id": obj.service.id_service,
            "name": obj.service.name,
            "description": obj.service.description
        }

    def create(self, validated_data):
        workshop_service = WorkshopsService.objects.create(
            workshop= validated_data['workshop_id'],
            service= validated_data['service_id'],
            price=validated_data['price']
        )
        return workshop_service


class BudgetsStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetsStatus
        fields = ['id_budget_status', 'name']

class BudgetSerializer(serializers.ModelSerializer):
    id_appointment = serializers.PrimaryKeyRelatedField(
        queryset=Appointments.objects.all(),
        required=True,
        help_text="The ID of the related appointment."
    )
    status = BudgetsStatusSerializer(read_only=True)

    class Meta:
        model = Budgets
        fields = ['id_budget','description', 'id_appointment', 'status' ,'created_at', 'amount']
        read_only_fields = ['id_budget', 'created_at', 'status']


    def create(self, validated_data):
        solicitud_enviada_status = BudgetsStatus.objects.get(name="Nuevo Prespuesto")
        budget = Budgets.objects.create(
            description=validated_data["description"],
            id_appointment=validated_data["id_appointment"],
            created_at=datetime.now(),
            status = solicitud_enviada_status,
            amount=validated_data['amount']
        )
        return budget


class BudgetStatusPatchSerializer(serializers.ModelSerializer):

    status = serializers.PrimaryKeyRelatedField(queryset=BudgetsStatus.objects.all(), write_only=True)
    budget_status_name = serializers.CharField(source='budget_status.name', read_only=True)

    def validate(self, data):
        current_status = self.instance.status
        new_status = data.get('budget_status')

        if current_status == new_status:
            raise serializers.ValidationError("The new status must be different from the current status.")

        return data

    class Meta:
        model = Budgets
        fields = [ 'budget_status_name', 'status']
