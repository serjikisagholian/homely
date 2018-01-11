from django.conf.urls import url, include
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'properties', views.PropertyViewSet, base_name='property')
router.register(r'reserves', views.ReserveViewSet, base_name='reserve')
router.register(r'homeowners', views.HomeownerViewSet, base_name='homeowner')
router.register(r'renters', views.RenterViewSet, base_name='renter')

rentals_patterns = [
    url('^$', views.index, name='rentals-list'),
    url(r'^', include(router.urls)),
]
