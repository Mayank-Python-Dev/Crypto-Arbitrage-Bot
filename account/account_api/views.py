from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.backends import TokenBackend
from account.account_api.serializers import (
    MyTokenObtainPairSerializer,
    ResetPasswordEmailSerializer
)
from account.models import (
    User
)
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class ForgetPassword(APIView):
   
    serializer_class = ResetPasswordEmailSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user_exists = User.objects.filter(email=email).exists()
        if user_exists:
            user = User.objects.get(email=email)
            if user:
                encoded_pk = urlsafe_base64_encode(force_bytes(user.user_uid))
                token = PasswordResetTokenGenerator().make_token(user)
                reset_url = reverse("forget-password",kwargs={"encoded_pk": encoded_pk, "token": token},)
                
                reset_link = f"http://127.0.0.1:3000{reset_url}"
                # email_body =f"Your password reset link: {reset_link}"
                # page_url = "http://infograinsdevelopment.com/marketplace/reset_pwd"

                # send_mail("Reset Your MarketPlace password",f"""Someone (hopefully you) has requested a password reset for your MarketPlace account.
                #  Follow the link to set a new password:{page_url}/{encoded_pk}/{token}""", 'kapilyadav@infograins.com', (user.email,),fail_silently=False)
                # send the rest_link as mail to the user.
                context = {
                    "status":status.HTTP_200_OK,
                    "success":True,
                    # "success":f'We have sent you a link to {user.email} to  reset your password',
                    "response":serializer.data,  
                    "reset_link": reset_link
                }

                return Response(context,status=status.HTTP_200_OK)
        else:
            context = {
                "status":status.HTTP_400_BAD_REQUEST,
                "success":False,
                "message":"User doesn't exists"
            }
            return Response(context,status=status.HTTP_400_BAD_REQUEST)

class ForgetPasswordAPI(APIView):
    """
    Verify and Reset Password Token View.
    """
    pass

    # serializer_class = ResetPasswordSerializer
	

    # def put(self, request, *args, **kwargs):
    #     try:
    #         serializer = self.serializer_class(data=request.data, context={"kwargs": kwargs})
    #         serializer.is_valid(raise_exception=True)
    #         context = {
    #             "status":status.HTTP_200_OK,
    #             "success":True,
    #             "message":"Password reset complete",
    #         }
    #         return Response(context,status=status.HTTP_200_OK)

    #     except Exception as exception:
    #         context = {
    #             "status":status.HTTP_400_BAD_REQUEST,
    #             "success":False,
    #             "response":serializer.errors
                
    #         }
    #     return Response(context,status=status.HTTP_400_BAD_REQUEST)