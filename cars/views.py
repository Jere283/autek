from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response

from cars.models import Cars
from cars.serializers import CarsSerializer


class GetAllCarsView(GenericAPIView):

    serializer_class = CarsSerializer

    def get (self, request):

        queryset = Cars.objects.all()
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)