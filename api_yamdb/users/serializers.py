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
