from django.core.management.base import BaseCommand, CommandError
import rentals.models as models

class Command(BaseCommand):
    help = 'Clear all data'

    def handle(self, *args, **options):
        ans = input('Are you sure delete all data?(Y/N)?')
        if ans.lower() != 'y': return
        models.Reserve.objects.all().delete()
        models.Property.objects.all().delete()
        models.Renter.objects.all().delete()
        models.Homeowner.objects.all().delete()
        self.stdout.write('All data has been removed')
