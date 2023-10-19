from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer


# Create your views here.


class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        # Получите данные пользователя из сериализатора
        user_data = serializer.validated_data

        # Создайте пользователя, установив пароль с использованием set_password
        user = User.objects.create_user(
            email=user_data['email'],
            password=user_data['password']
        )

        user.save()

        return Response({'detail': 'Пользователь успешно зарегистрирован.'}, status=status.HTTP_201_CREATED)
