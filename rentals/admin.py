from django.contrib import admin
from .models import Homeowner, Renter, Property, Reserve
# from .forms import ReserveAdminForm


@admin.register(Homeowner)
class HomeownerAdmin(admin.ModelAdmin):
    list_display = ['username','email','cell_phone']


@admin.register(Renter)
class RenterAdmin(admin.ModelAdmin):
    list_display = ['username','email','cell_phone']


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['homeowner','address','baths','rooms','furnished','is_active']


@admin.register(Reserve)
class ReserveAdmin(admin.ModelAdmin):
    # form = ReserveAdminForm
    list_display = ['pk','start_date','end_date','renter','property']
