import re

from rest_framework import serializers

from .models import *


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['email', 'fam', 'name', 'otc', 'phone']

    def validate_phone(self, phone):
        regex=r'^\+7 \(\d{3}\) \d{3}-\d\d-\d\d$'
        if not re.match(regex, phone):
            raise serializers.ValidationError('Телефон должен быть в формате: +7 (xxx) xxx-xx-xx')
        return phone
    
    def validate(self, data):
        email = data.get('email')
        fam = data.get('fam')
        name = data.get('name')
        otc = data.get('otc')
        phone = data.get('phone')

        existing_user = User.objects.filter(models.Q(email=email) | models.Q(phone=phone)).first()

        if existing_user:
            if (existing_user.fam != fam or
                existing_user.name != name or
                (existing_user.otc or '') != (otc or '')):
                raise serializers.ValidationError({
                    'user': 'Пользователь с таким email или телефоном уже существует, но данные не совпадают. Изменение данных запрещено.'
                })
        return data
    

class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['latitude', 'longitude', 'height',]
    

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['winter', 'summer', 'autumn', 'spring',]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['data', 'title']
    

class PassSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer()
    images = ImageSerializer(many=True, required=False)

    class Meta:
        model = Pass
        fields = ['id', 'beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'user', 'coords', 'level', 'images']

