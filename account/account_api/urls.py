from django.urls import path
from account.account_api.views import (
    MyObtainTokenPairView,
    ForgetPassword,
    ForgetPasswordAPI
)

urlpatterns = [

    path("login/",MyObtainTokenPairView.as_view(),name="account-login"),
    path("forget-password-link/",ForgetPassword.as_view(),name="request-forget-password"),
    path("forget-reset/<str:encoded_pk>/<str:token>/",ForgetPasswordAPI.as_view(),name="forget-password"),
    
]