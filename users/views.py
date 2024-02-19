from rest_framework import generics

from users.models import User
from users.serialisers import UserSerializer

class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        new_user = serializer.save()
        password = serializer.data["password"]
        new_user.set_password(password)
        new_user.save()


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


    def perform_update(self, serializer):
        new_user = serializer.save()
        password = serializer.data["password"]
        new_user.set_password(password)
        new_user.save()


class UserDestroyAPIView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()



class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()



class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()



