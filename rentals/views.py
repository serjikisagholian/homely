from django.shortcuts import render

import datetime
from django.db.models import Q
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.exceptions import APIException
from rest_framework import status

from .serializers import HomeownerSerializer, RenterSerializer, PropertySerializer, ReserveSerializer
from .models import Homeowner, Renter, Property, Reserve


def index(request):
    return render(
        request,
        'rentals/index.html',
        context={}
    )


class BadRequestException(APIException):
    status_code = 400


def get_date_from_qs(str_date):
    try:
        # dl = [str_date[0:4],str_date[4:6],str_date[6:8],str_date[8:10],str_date[10:12],str_date[12:14]]
        # y,mo,dd,hh,mm,ss= list(map(int, dl))
        print(str_date)
        dl = [str_date[0:4],str_date[4:6],str_date[6:8]]
        y,mo,dd = list(map(int, dl))
        # return datetime.datetime(y,mo,dd,hh,mm,ss)
        return datetime.datetime(y,mo,dd)
    except Exception as e:
        print(e)
        raise BadRequestException("Error parsing input dates")


class HomeownerViewSet(viewsets.ModelViewSet):
    serializer_class = HomeownerSerializer
    queryset = Homeowner.objects.all()
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['get', 'post', 'head','patch','delete']


class RenterViewSet(viewsets.ModelViewSet):
    serializer_class = RenterSerializer
    queryset = Renter.objects.all()
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['get', 'post', 'head','patch','delete']


class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    http_method_names = ['get', 'post', 'head','patch','delete']
    def get_queryset(self):
        if not 'start' in self.request.query_params:
            return Property.objects.filter(is_active=True)
        else:
            start = get_date_from_qs(self.request.query_params['start'])
            end = get_date_from_qs(self.request.query_params['end'])
            return Property.search_available(start,end)

class ReserveViewSet(viewsets.ModelViewSet):
    serializer_class = ReserveSerializer
    http_method_names = ['get', 'post', 'head','patch','delete']
    def get_queryset(self):
        return Reserve.objects.all()
