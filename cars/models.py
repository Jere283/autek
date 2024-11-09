from django.db import models

from users.models import User


class CarBrand(models.Model):
    id_brand = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'car_brands'


class CarModel(models.Model):
    id_model = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'car_models'





class Color(models.Model):
    id_color = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=60)

    class Meta:
        managed = False
        db_table = 'colors'


class Car(models.Model):
    id_car = models.AutoField(primary_key=True)
    brand = models.ForeignKey(CarBrand, models.DO_NOTHING)
    model = models.ForeignKey(CarModel, models.DO_NOTHING)
    color = models.ForeignKey(Color, models.DO_NOTHING)
    license_plate = models.CharField(unique=True, max_length=15)
    year = models.CharField(max_length=4)
    user = models.ForeignKey(User, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cars'