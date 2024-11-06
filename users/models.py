from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import validate_email
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):

    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("Ingresa un correo electronico valido")

    def create_user(self, id, email, first_name, last_name, password, **extra_fields):
        if not email:
            raise ValueError('Se necesita un correo electronico')
        email = self.normalize_email(email)
        self.email_validator(email)

        if not first_name:
            raise ValueError('Se necesita un primer nombre')
        if not last_name:
            raise ValueError('Se necesita un apellido')

        user = self.model(id=id, email=email, first_name=first_name,
                          last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, id, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self.create_user(
            id, email, first_name, last_name, password, **extra_fields
        )
        user.save(using=self._db)

        return user
class Roles(models.Model):
    id_role = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=60)

    class Meta:
        ##managed = False
        db_table = 'roles'


class User(AbstractBaseUser, PermissionsMixin):

    id = models.CharField(primary_key=True, max_length=14)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(unique=True, max_length=120)
    password = models.CharField(max_length=200)
    date_of_birth = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)
    role = models.ForeignKey(Roles, models.DO_NOTHING, db_column='role', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['id', 'first_name', 'last_name']

    class Meta:
        ##managed = False
        db_table = 'users'

    def __str__(self):
        return self.id

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }