from rest_framework.views import APIView
from wypozyczalnia.serializers import LoginSerializer, RegisterSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from knox.auth import AuthToken
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth.models import User



class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = AuthToken.objects.create(user=user)[1]
        return Response({
            'token': token,
            'user': UserSerializer(user,context=self.get_serializer_context()).data
        })

class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = AuthToken.objects.create(user=user)[1] 
        print(token)
        return Response({
            'token': token,
            'user': UserSerializer(user,context=self.get_serializer_context()).data
        })

class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)