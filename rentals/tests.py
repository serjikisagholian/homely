import sys
import logging
from datetime import datetime, timedelta
# from django.core.management import call_command
from django.http import Http404
from django.contrib.auth import authenticate
from rest_framework.test import APIClient, APITestCase
from rest_framework.reverse import reverse
from rest_framework_jwt.settings import api_settings

from .models import *
from .serializers import *


class Account(object):
    def __init__(self):
        self.csrf_client = APIClient(enforce_csrf_checks=True)

    def create_token(self, user):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def login(self,username,password):
        user = authenticate(username=username, password=password)
        if user:
            token = self.create_token(user)
            return token
        else:
            return None


class ReserveTests(APITestCase):
    fixtures = ['homely_test']

    def setUp(self):
        # test does not wait for this
        # call_command('createfakedata', 5, verbosity=0, database='default')
        logging.basicConfig( stream=sys.stderr )
        logging.getLogger( "Test.test" ).setLevel( logging.DEBUG )
        self.log = logging.getLogger( "Test.test" )
        self.csrf_client = APIClient(enforce_csrf_checks=True)
        self.user1 = UserProfile.objects.first()
        self.csrf_client.force_authenticate(self.user1)
        self.auth_token = Account().login(self.user1.username, self.user1.username)

    def test_properties_list(self):
        url = reverse('property-list')
        response = self.csrf_client.get(url)
        self.assertEqual(response.status_code, 200)
        count = Property.objects.all().count()
        self.assertEqual(response.data.get('count'), count)

    def test_reserve(self):
        start = datetime(2018,2,1)
        end = datetime(2018,2,2)
        property = Property.search_available(start,end)[0]
        renter = Renter.objects.first()

        self.csrf_client.force_authenticate(self.user1)
        data = {'property': property.id, 'renter': renter.id,'start_date': '2018-02-01', 'end_date':'2018-02-02'}
        url = reverse('reserve-list')
        response = self.csrf_client.post(url, data)
        self.assertEqual(response.status_code, 201)
