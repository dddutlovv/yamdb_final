from django.urls import path

from .views import get_jwt_token, register_user

urlpatterns = [
    path('signup/', register_user, name='registration'),
    path('token/', get_jwt_token, name='token'),
]
