from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}} # Never return the password

    def create(self, validated_data):
        # Use create_user instead of create to hash the password
        user = User.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user