from django.core.management.base import BaseCommand, CommandError
import rentals.models as models
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Generate Fake data using faker'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    def handle(self, *args, **options):
        count = int(options['count'])

        faker = Faker()
        for i in range(0,count):
            self.stdout.write("Creating iteration : %s" %(i))
            self.create_homeowner(faker)
            self.create_renter(faker)

        # I want to creare Properties after homeowner creation
        # So I can pick a random ForeignKey
        buffer_count = 50
        for i in range(0,count):
            self.stdout.write("Creating iteration : %s" %(i))
            if i % buffer_count == 0:
                limit = i + buffer_count
                homeowners = models.Homeowner.objects.all()[i:limit]

            self.create_property(faker,homeowners)

        self.stdout.write("Fake records successfully created")

    def create_homeowner(self,faker):
        try:
            owner = models.Homeowner()
            owner.username = faker.user_name()
            owner.password = owner.username # Just for convenience faker.password()
            owner.email = faker.email()
            owner.cell_phone = "818{0}".format(random.randint(1000000,9999999))
            owner.save()
            self.stdout.write('Owner: %s created' % (owner))
        except Exception as e:
            self.stdout.write('Execption occured in creating Owner: %s' % (e.__str__()))

    def create_renter(self,faker):
        try:
            renter = models.Renter()
            renter.username = faker.user_name()
            renter.password = renter.username # Just for convenience faker.password()
            # user.auth_token = faker.md5()
            renter.email = faker.email()
            renter.cell_phone = "818{0}".format(random.randint(1000000,9999999))
            renter.save()
            self.stdout.write('Renter: %s created' % (renter))
        except Exception as e:
            self.stdout.write('Execption occured in creating Renter: %s' % (e.__str__()))

    def create_property(self, faker,homeowners):
        try:
            myproperty = models.Property()
            myproperty.homeowner = homeowners[random.randint(0,len(homeowners)-1)]
            myproperty.save()
            self.stdout.write('Property: %s created' % (myproperty))
        except Exception as e:
            self.stdout.write('Execption occured in creating Property: %s' % (e.__str__()))
