from rest_framework import serializers

from cars.models import CarModel, CarBrand, Car, Color
from users.models import User
from users.serializers import UserRegisterSerializer
import logging

logger = logging.getLogger(__name__)


class CarModelsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarModel
        fields = ['id_model', 'name']

class CarBrandsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarBrand
        fields =['id_brand', 'name']

class CarColorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color
        fields =['id_color', 'name']


class CarsSerializer(serializers.ModelSerializer):

    brand_id = serializers.PrimaryKeyRelatedField(queryset=CarBrand.objects.all(), write_only=True)
    model_id = serializers.PrimaryKeyRelatedField(queryset=CarModel.objects.all(), write_only=True)
    color_id = serializers.PrimaryKeyRelatedField(queryset=Color.objects.all(), write_only=True)


    brand = CarBrandsSerializer(read_only=True)
    model = CarModelsSerializer(read_only=True)
    color = CarColorsSerializer(read_only=True)
    user = UserRegisterSerializer(read_only=True)

    class Meta:
        model = Car
        fields = ['id_car', 'brand', 'model', 'color', 'brand_id', 'model_id', 'color_id','license_plate', 'year', 'user']

    def validate(self, attrs):
        print("User:", self.context['request'].user)
        return attrs


    def create(self, validated_data):
        user = self.context['request'].user
        logger.debug(f"Creating car with user: {user}")

        car = Car.objects.create(
            brand_id=validated_data['brand_id'].id_brand,
            model_id=validated_data['model_id'].id_model,
            color_id=validated_data['color_id'].id_color,
            license_plate=validated_data['license_plate'],
            year=validated_data['year'],
            user =user
        )
        return car