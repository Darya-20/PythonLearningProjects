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
        model = Coords
        fields = ['latitude', 'longitude', 'height',]

    def validate_latitude(self, value):
        if value < -90 or value > 90:
            raise serializers.ValidationError("Широта должна быть в диапазоне [-90, 90]")
        return value

    def validate_longitude(self, value):
        if value < -180 or value > 180:
            raise serializers.ValidationError("Долгота должна быть в диапазоне [-180, 180]")
        return value
    

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
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

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        level_data = validated_data.pop('level')
        images_data = validated_data.pop('images', [])

        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        coords = Coords.objects.create(**coords_data)

        level = Level.objects.create(**level_data)

        pass_obj = Pass.objects.create(
            user=user,
            coords=coords,
            level=level,
            **validated_data
        )

        for image_data in images_data:
            Image.objects.create(pass_obj=pass_obj, **image_data)

        return pass_obj