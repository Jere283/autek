from django.db import models

from cars.models import Car
from users.models import User
from workshops.models import Workshop


class Service(models.Model):
    id_service = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'services'


class AppointmentStatus(models.Model):
    id_appointment_status = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=60)

    class Meta:
        managed = False
        db_table = 'appointment_status'


class Appointments(models.Model):
    id_appointment = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    car = models.ForeignKey(Car, models.DO_NOTHING, db_column='id_car', blank=True, null=True)
    workshops = models.ForeignKey(Workshop, models.DO_NOTHING, db_column='id_workshops', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField()
    appointment_status = models.ForeignKey(AppointmentStatus, models.DO_NOTHING, db_column='appointment_status', blank=True, null=True)
    approved_budget = models.DecimalField(max_digits=14, decimal_places=2, null=False)

    class Meta:
        managed = False
        db_table = 'appointments'

class AppointmentsImages(models.Model):
    id_image = models.AutoField(primary_key=True)
    id_appointment = models.ForeignKey(Appointments, models.DO_NOTHING, db_column='id_appointment')
    url = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'appointments_images'


class WorkshopsService(models.Model):
    id_workshop_service = models.AutoField(primary_key=True)
    workshop = models.ForeignKey(Workshop, models.DO_NOTHING)
    service = models.ForeignKey(Service, models.DO_NOTHING)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'workshops_services'



class AppointmentsServices(models.Model):
    id_appointment_service = models.AutoField(primary_key=True)
    appointment = models.ForeignKey(Appointments, models.DO_NOTHING)
    service = models.ForeignKey(WorkshopsService, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'appointments_services'


class BudgetsStatus(models.Model):
    id_budget_status = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=60)

    class Meta:
        managed = False
        db_table = 'budgets_status'


class Budgets(models.Model):
    id_budget = models.AutoField(primary_key=True)
    description = models.CharField(max_length=200)
    id_appointment = models.ForeignKey(Appointments, models.DO_NOTHING, db_column='appointment_id')
    status = models.ForeignKey(BudgetsStatus, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2, null=False)

    class Meta:
        managed = False
        db_table = 'budgets'
