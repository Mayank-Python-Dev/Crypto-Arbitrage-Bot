from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import status
from account.models import (
    User
)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        email = attrs.get("email", None)
        password = attrs.get("password", None)
        try:
            user_instance = User.objects.get(email__iexact=email)
            
        except Exception as exception:
            return {
                "status":status.HTTP_401_UNAUTHORIZED,
                "error_status":True,
                "error":"User is not exists. Please Register first!"
            }
        user = authenticate(email=email, password=password)
        if user is not None:
            if user_instance.is_superuser:
                refresh = self.get_token(user)
                
                return {
                    "status":status.HTTP_200_OK,
                    "error_status":False,
                    "refresh":str(refresh),
                    "access":str(refresh.access_token),
                    "username":user_instance.username,
                    "email":user_instance.email,
                    "user_uid":user.user_uid
                }
            else:
                return {
                    'status':status.HTTP_400_BAD_REQUEST,
                    'error_status':True,
                    'response':"You are not authorized to access"
            }
        elif user is None:
            return {
                "status":status.HTTP_401_UNAUTHORIZED,
                "error_status":True,
                "error":"Incorrect Password!"
            }
             
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['username'] = user.username
        return token


    
class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']