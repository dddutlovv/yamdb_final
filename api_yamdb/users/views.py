from rest_framework import viewsets
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import filters
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import (JwtTokenSerializer,
                          RegistrationSerializer,
                          UserOwnInfoSerializer,
                          UserSerializer)
from .models import User
from .permissions import IsAdmin

account_activation_token = PasswordResetTokenGenerator()


class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = get_object_or_404(
                User,
                username=serializer.validated_data['username']
            )
            code = account_activation_token.make_token(user=user)
            send_mail(
                subject='Авторизация в YAMDB API',
                message=f'{user.username}, ваш код для авторизации: {code}',
                from_email='reg@yamdb.com',
                recipient_list=[user.email]
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif User.objects.filter(username=request.data.get('username'),
                                 email=request.data.get('email')).exists():
            user = User.objects.get(username=request.data.get('username'))
            code = account_activation_token.make_token(user=user)
            send_mail(
                subject='Авторизация в YAMDB API',
                message=f'{user.username}, ваш код для авторизации: {code}',
                from_email='reg@yamdb.com',
                recipient_list=[user.email]
            )
            return Response(request.data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class TokenViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = JwtTokenSerializer
    permission_classes = [AllowAny, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User,
                username=serializer.validated_data['username']
            )

            if account_activation_token.check_token(
                    user,
                    serializer.validated_data['confirmation_code']):
                token = str(AccessToken.for_user(user))
                return Response({'token': token}, status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(detail=False,
            methods=['get', 'patch'],
            url_path='me',
            permission_classes=[IsAuthenticated])
    def get_user_own_info(self, request):
        user = request.user
        if request.method == "PATCH":
            serializer = UserOwnInfoSerializer(
                user,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            serializer = UserOwnInfoSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
