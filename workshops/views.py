from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from workshops.models import Workshop
from workshops.serializers import WorkshopSerializer


class GetWorkshopsView(GenericAPIView):
    serializer_class = WorkshopSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, workshop_id=None ):
        try:
            if workshop_id != None:
                queryset = Workshop.objects.filter(id_workshop=workshop_id)

            else:
                queryset = Workshop.objects.all()

            serializer = self.serializer_class(queryset, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetWorkshopsByIdView(GenericAPIView):
    serializer_class = WorkshopSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, workshop_id=None ):
        try:
            queryset = get_object_or_404(Workshop,id_workshop=workshop_id)


            serializer = self.serializer_class(queryset)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


