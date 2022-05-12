from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        if self.validated_data['username'] == 'me':
            raise serializers.ValidationError('Can\'t use these username')
        return User.objects.create(**validated_data)

    class Meta:
        model = User
        fields = ('email', 'username')


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=100)
