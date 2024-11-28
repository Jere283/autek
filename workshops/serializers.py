from rest_framework import serializers
from .models import Country, State, City, Address, Workshop


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id_country', 'name']


class StateSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)

    class Meta:
        model = State
        fields = ['id_state', 'name', 'country']


class CitySerializer(serializers.ModelSerializer):
    state = StateSerializer(read_only=True)

    class Meta:
        model = City
        fields = ['id_city', 'name', 'state']


class AddressSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)

    class Meta:
        model = Address
        fields = ['id_address', 'city', 'address']


class WorkshopSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    address_id = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all(), write_only=True)

    class Meta:
        model = Workshop
        fields = ['id_workshop', 'name', 'phone_number', 'email', 'address', 'address_id', 'rating']

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        workshop = Workshop.object.create(
            name=validated_data['name'],
            phone_number=validated_data['phone_number'],
            email=validated_data['email'],
            address_id=validated_data['adress_id'].id_adress
        )

        return workshop
