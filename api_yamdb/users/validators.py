import re

from rest_framework import serializers

pattern = re.compile('^[\\w.@+-]+')


def user_name_validator(value):
    if value.lower() == 'me':
        raise serializers.ValidationError('Запрещенное имя пользователя')

    if not pattern.match(value):
        raise serializers.ValidationError('Имя может содержать только буквы,',
                                          'цифры и символы @/./+/-/_ ')
