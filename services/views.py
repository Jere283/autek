from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from services.models import Appointments
from services.serializers import AppointmentsSerializer


class CreateAppointmentView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = AppointmentsSerializer


    def post(self, request):
        print(request.data)
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
                                           )
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()

                return Response(data={
                    "data": serializer.data,
                    'message': "The appointment has been created."
                }, status=status.HTTP_201_CREATED)
            return Response(data={"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetAllAppointmentsView(GenericAPIView):
    serializer_class = AppointmentsSerializer

    def get(self, request):
        try:
            # Use select_related to optimize fetching related objects (user, car, workshop)
            queryset = Appointments.objects.select_related(
                'user',  # join with user table
                'car',  # join with car table
                'workshops'  # join with workshops table
            ).all()

            serializer = self.serializer_class(queryset, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)