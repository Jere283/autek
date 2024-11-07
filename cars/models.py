from django.db import models

class CarBrands(models.Model):
    id_brand = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'car_brands'


class CarModels(models.Model):
    id_model = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'car_models'


class Cars(models.Model):
    id_car = models.AutoField(primary_key=True)
    brand = models.ForeignKey(CarBrands, models.DO_NOTHING)
    model = models.ForeignKey(CarModels, models.DO_NOTHING)
    color = models.ForeignKey('Colors', models.DO_NOTHING)
    license_plate = models.CharField(unique=True, max_length=15)
    year = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'cars'


class Colors(models.Model):
    id_color = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=60)

    class Meta:
        managed = False
        db_table = 'colors'
