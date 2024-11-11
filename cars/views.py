from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cars.models import Car
from cars.serializers import CarsSerializer
from users.models import User


class GetAllCarsView(GenericAPIView):

    serializer_class = CarsSerializer

    def get (self, request):
        try:
            queryset = Car.objects.all()
            serializer = self.serializer_class(queryset, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CreateCarsView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class =  CarsSerializer

    def post(self, request):

        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
                                           )
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()

                return Response(data={
                    "data": serializer.data,
                    'message': "The vehicle has been created."
                }, status=status.HTTP_201_CREATED)
            return Response(data={"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("User:", request.user)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class GetUserCarsView(GenericAPIView):
    serializer_class = CarsSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id=None ):
        try:
            if user_id != None:
                user = get_object_or_404(User, id=user_id)
                queryset = Car.objects.select_related(
                    'brand',
                    'model',
                    'color',
                    'user'
                ).filter(user=user)

            else:
                queryset = Car.objects.select_related(
                    'brand',
                    'model',
                    'color',
                    'user'
                ).filter(user=request.user)

            serializer = self.serializer_class(queryset, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
