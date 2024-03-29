from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView

from main.permissions import UserOwner, Moderator
from users.models import User
from users.serialisers import UserSerializer, MyTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    # permission_classes = [UserOwner]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        new_user = serializer.save()
        password = serializer.data["password"]
        new_user.set_password(password)
        new_user.save()


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [UserOwner]


    def perform_update(self, serializer):
        new_user = serializer.save()
        password = serializer.data["password"]
        new_user.set_password(password)
        new_user.save()


class UserDestroyAPIView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, UserOwner]



class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, Moderator | UserOwner]



class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer