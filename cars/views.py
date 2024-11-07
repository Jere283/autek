from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response

from cars.models import Cars
from cars.serializers import CarsSerializer


class GetAllCarsView(GenericAPIView):

    serializer_class = CarsSerializer

    def get (self, request):
        try:
            queryset = Cars.objects.all()
            serializer = self.serializer_class(queryset, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CreateCarsView(GenericAPIView):

    serializer_class =  CarsSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()

                return Response(data={
                    "data": serializer.data,
                    'message': "The vehicle has been created."
                }, status=status.HTTP_201_CREATED)
            return Response(data={"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
