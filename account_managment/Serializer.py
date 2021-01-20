from rest_framework.serializers import Serializer
from rest_framework import serializers
from .models import *
class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['phone', 'first_name','id']


class SellerInformationGetSerializer(serializers.ModelSerializer):


    class Meta:
        model = FoofRoofSellerInformation
        fields = '__all__'


class CustomerInfoSerializer(serializers.ModelSerializer):
    phone = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomerInfo
        fields = '__all__'

    def get_phone(self, obj):
        return obj.user.phone