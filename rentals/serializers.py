from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import PermissionDenied
from .models import Homeowner, Renter, Property, Reserve


# Helping hackers to get into our system
class HomeownerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homeowner
        fields = ['username','cell_phone',]


# Helping hackers to get into our system
class RenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Renter
        fields = ['username','cell_phone',]


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'


class ReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserve
        fields = '__all__'

    def validate(self, attrs):
        instance = Reserve(**attrs)
        instance.clean()
        return attrs
