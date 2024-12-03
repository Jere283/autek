from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from autek.permissions import IsAdmin
from services.models import Appointments, AppointmentStatus
from services.serializers import AppointmentsSerializer, AppointmentStatusSerializer, AppointmentStatusPatchSerializer
from users.models import User


class CreateAppointmentView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = AppointmentsSerializer


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
                    'message': "The appointment has been created."
                }, status=status.HTTP_201_CREATED)
            return Response(data={"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetAllAppointmentsView(GenericAPIView):
    serializer_class = AppointmentsSerializer

    def get(self, request):
        try:
            status_name = request.query_params.get('status')

            queryset = Appointments.objects.select_related('user', 'car', 'workshops', 'appointment_status')

            if status_name:
                queryset = queryset.filter(appointment_status__name=status_name)

            serializer = self.serializer_class(queryset, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetAppointmentByIdView(GenericAPIView):
    serializer_class = AppointmentsSerializer

    def get(self, request, id=None):
        try:

            appointment = Appointments.objects.select_related('user', 'car', 'workshops').get(id_appointment=id)

            serializer = self.serializer_class(appointment)
            if not appointment:
                return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

#TODO: Admin Role Only
class GetAllAppointmentsStatusView(GenericAPIView):
    serializer_class = AppointmentStatusSerializer
    def get(self, request):
        try:
            queryset = AppointmentStatus.objects.all()
            serializer = self.serializer_class(queryset, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


#TODO: limit the user ID serach only to admins when implementing roles
class GetUserAppointmentsView(GenericAPIView):
    serializer_class = AppointmentsSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id=None ):
        try:
            if user_id != None:
                user = get_object_or_404(User, id=user_id)
                queryset = Appointments.objects.select_related(
                    'user',
                    'car',
                    'workshops'
                ).filter(user=user)

            else:
                queryset = Appointments.objects.select_related(
                    'user',
                    'car',
                    'workshops'
                ).filter(user=request.user)

            serializer = self.serializer_class(queryset, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class AppointmentStatusUpdateView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdmin ]

    def patch(self, request, appointment_id):
        try:
            appointment = Appointments.objects.get(pk=appointment_id)
        except Appointments.DoesNotExist:
            return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AppointmentStatusPatchSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Appointment status updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)