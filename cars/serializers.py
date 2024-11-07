from rest_framework import serializers

from cars.models import CarModels, CarBrands, Cars, Colors


class CarModelsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarModels
        fields = ['id_model', 'name']

class CarBrandsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarBrands
        fields =['id_brand', 'name']

class CarColorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Colors
        fields =['id_color', 'name']


class CarsSerializer(serializers.ModelSerializer):

    brand_id = serializers.PrimaryKeyRelatedField(queryset=CarBrands.objects.all(), write_only=True)
    model_id = serializers.PrimaryKeyRelatedField(queryset=CarModels.objects.all(), write_only=True)
    color_id = serializers.PrimaryKeyRelatedField(queryset=Colors.objects.all(), write_only=True)

    brand = CarBrandsSerializer(read_only=True)
    model = CarModelsSerializer(read_only=True)
    color = CarColorsSerializer(read_only=True)

    class Meta:
        model = Cars
        fields = ['id_car', 'brand', 'model', 'color', 'brand_id', 'model_id', 'color_id','license_plate', 'year']

    def validators(self, attrs):
        return attrs

    def create(self, validated_data):
        car = Cars.objects.create(
            brand = validated_data['brand'],
            model = validated_data['model'],
            color = validated_data['color'],
            license_plate = validated_data['license_plate'],
            year = validated_data['year']
        )
        return car