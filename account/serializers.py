from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['mobile', 'first_name', 'last_name', 'password', 'password_confirm']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        # Add mobile number validation logic if necessary
        mobile = attrs.get('mobile')
        if len(mobile) != 10:
            raise serializers.ValidationError({"mobile": "Mobile number must be 10 digits."})
        if not mobile.isdigit():
            raise serializers.ValidationError({"mobile": "Mobile number must contain only digits."})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create(
            username=validated_data['mobile'],
            mobile=validated_data['mobile'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        mobile = data.get('mobile')
        password = data.get('password')

        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            raise serializers.ValidationError({"mobile": "Mobile number not found."})

        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Incorrect password."})

        data['user'] = user
        return data
