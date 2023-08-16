from rest_framework import serializers

import Pet.serializer
from .models import User
from .models import Schedule

class UserSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # write_only로 설정하여 응답에 비밀번호가 포함되지 않도록 합니다.

    class Meta:
        model = User
        fields = ['user_id', 'username', 'gender', 'phone', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # 비밀번호를 암호화하여 저장합니다.
        user.save()
        return user


class UserAndPetSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'gender', 'phone']


class ScheduleSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'diary_date', 'etc']
