from account_managment.views import *
from django.urls import include, path
from knox import views as knox_views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()



auth_urlpatterns = [
    path("login/", LoginView.as_view(), name="knox_login"),

    # path("otp_auth/", OtpSignUpView.as_view(), name="otp_login"),
    # path("get_otp/<str:phone>/",
    #      UserAccountManagerViewSet.as_view({'get': 'get_otp'}), name="get_otp"),

    path("logout/", knox_views.LogoutView.as_view(), name="knox_logout"),
    # path("reset_password/", reset_password),
    # path("change_password/",
    #      ChangePasswordViewSet.as_view({"post": "create"})),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path("verify/", verify_login, name="verify_token"),
]

urlpatterns=[
    path('',include(router.urls)),
    path("auth/", include(auth_urlpatterns), name="auth"),
]