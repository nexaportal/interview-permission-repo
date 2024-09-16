from account.models.user import User

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator


from .validators import CustomPasswordValidator, MobileValidator


'''
    Serializer That Create Token with simple jwt library
'''
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['mobile'] = (user.mobile).lower()
        return token
    

'''
    Serializer To Handle User object creation, user password will be hashed
'''
class RegisterSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all(), message='Phone Number is used before'), 
            MobileValidator()
    ])
    email = serializers.EmailField(
        required=False,
        validators=[
            UniqueValidator(queryset=User.objects.all(), message='Email Is used Before')
    ])
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=
        [CustomPasswordValidator()
    ])
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id', 'password', 'email', 'mobile', 'first_name', 'last_name')
        extra_kwargs = {
            'id': {'required': False},
            'email': {'required': False},
            'password': {'required': True},
            'mobile': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }


    def create(self, validated_data):
        user = User.objects.create(
            **validated_data
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
