from datetime import timezone

from django.contrib.auth import login
from django.contrib.auth.signals import user_logged_in
from drf_yasg2.utils import swagger_auto_schema
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions, status, viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from utils.response_wrapper import ResponseWrapper
from account_managment.Serializer import *

def login_related_info(user):
    user_serializer = UserAccountSerializer(instance=user)
    seller_info = []
    customer_info = None
    try:
        if user.hotel_staff.first():
            seller_info_serializer = SellerInformationGetSerializer(
                instance=user.hotel_staff.all(), many=True)
            seller_info = seller_info_serializer.data
    except:
        pass
    try:
        if user.customer_info:
            customer_info_serialzier = CustomerInfoSerializer(
                instance=user.customer_info)
            customer_info = customer_info_serialzier.data
    except:
        pass
    return customer_info, seller_info, user_serializer

class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = AuthTokenSerializer

    @swagger_auto_schema(request_body=AuthTokenSerializer)
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)

        token_limit_per_user = self.get_token_limit_per_user()
        if token_limit_per_user is not None:
            now = timezone.now()
            token = request.user.auth_token_set.filter(expiry__gt=now)
            if token.count() >= token_limit_per_user:
                return Response(
                    {"error": "Maximum amount of tokens allowed per user exceeded."},
                    status=status.HTTP_403_FORBIDDEN
                )
        token_ttl = self.get_token_ttl()
        instance, token = AuthToken.objects.create(request.user, token_ttl)
        user_logged_in.send(sender=request.user.__class__,
                            request=request, user=request.user)
        data = self.get_post_response_data(request, token, instance)
        customer_info, staff_info, user_serializer = login_related_info(user)
        return ResponseWrapper(data={'auth': data, 'user': user_serializer.data, 'staff_info': staff_info, 'customer_info': customer_info})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_login(request):
    return ResponseWrapper(data="Token is Valid", status=200)
