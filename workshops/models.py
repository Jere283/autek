from django.db import models


class Country(models.Model):
    id_country = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'country'


class State(models.Model):
    id_state = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=80)
    country = models.ForeignKey(Country, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'states'


class City(models.Model):
    id_city = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=80)
    state = models.ForeignKey(State, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cities'


class Address(models.Model):
    id_address = models.AutoField(primary_key=True)
    city = models.ForeignKey(City, models.DO_NOTHING, blank=True, null=True)
    address = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'addresses'


class Workshop(models.Model):
    id_workshop = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    phone_number = models.CharField(max_length=10)
    email = models.CharField(unique=True, max_length=120)
    address = models.ForeignKey(Address, models.DO_NOTHING, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'workshops'


