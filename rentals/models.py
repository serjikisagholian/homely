from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User as DjangoUser
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.core.exceptions import ValidationError


class UserProfile(DjangoUser):
    '''
    This is extended version of Django User
    I have just added cellphone and validated it
    with Los Angeles Area (Just as a sample)
    '''

    cell_phone = models.CharField(max_length=10,unique=True, null=True,
	blank=True, validators = [
        RegexValidator(
            regex='^818[0-9]*$',
            message='contact_no must be Numeric',
            code='invalid_contact_no'
        )
    ], verbose_name = 'Cellphone')

    def __str__(self):
        return self.username

class Homeowner(UserProfile):
    '''
    Add extra fields needed by Homeowner
    '''
    class Meta:
        verbose_name = 'Homeowner'
        verbose_name_plural = 'Homeowners'
        ordering = ['-id']


class Renter(UserProfile):
    '''
    Add extra fields as Renter
    '''
    class Meta:
        verbose_name = 'Renter'
        verbose_name_plural = 'Renters'
        ordering = ['-id']

@receiver(pre_save, sender=UserProfile)
@receiver(pre_save, sender=Homeowner)
@receiver(pre_save, sender=Renter)
def user_profile_pre_save(sender, instance, **kwargs):
    if instance.pk is None:   # insert
        instance.set_password(instance.password)
    elif instance.password:  # update_mode and password not None
        u = UserProfile.objects.get(pk=instance.pk)
        if u.password != instance.password: # new password entered
            instance.set_password(instance.password)


class Property(models.Model):
    homeowner = models.ForeignKey(Homeowner, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    baths = models.IntegerField(default=0)
    rooms = models.IntegerField(default=0)
    furnished = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
        ordering = ['-id']

    def __str__(self):
        return str(self.pk)

    @staticmethod
    def search_available(start, end):
        reserve_ids = Reserve.objects.filter(Q(start_date__range=(start,end)) | \
            Q(end_date__range=(start,end))
        ).values_list('property_id', flat=True)
        return Property.objects.filter(Q(is_active=True), ~Q(pk__in=reserve_ids))


class Reserve(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Reserve'
        verbose_name_plural = 'Reserves'
        ordering = ['-id']

    def clean(self):
        found = Reserve.objects.filter(Q(property=self.property), \
            (Q(start_date__gte=self.start_date, start_date__lte=self.end_date) \
            | Q(end_date__gte=self.start_date, end_date__lte=self.end_date)))
        if self.pk:
            found = found.exclude(pk=self.pk)

        if found.count() > 0:
           raise ValidationError("No Vacancy on selected range")
