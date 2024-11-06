from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.serializers import LoginSerializer, UserRegisterSerializer


class RegisterUserView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_data = serializer.data
            return Response({
                'data': user_data,
                'message': f"Gracias por registrate"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class profile(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  
        data = {
            'id': user.id,
            'email': user.email,
            'username': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'profile_img': user.profile_img
        }
        return Response(data, status=status.HTTP_200_OK)
