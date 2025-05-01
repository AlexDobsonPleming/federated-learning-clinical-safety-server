from django.core.management.base import BaseCommand
from api.models import FlModel

class Command(BaseCommand):
    help = 'Seed database: leave only one FlModel entry'

    def handle(self, *args, **options):
        # Remove all existing entries
        FlModel.objects.all().delete()

        # Add single seeded model
        FlModel.objects.create(
            name='Initial Model',
            accuracy=0.69,
            generalisability=0.057,
            security=None,
        )

        self.stdout.write(self.style.SUCCESS(
            'Database seeded: single FlModel with accuracy=0.69, generalisability=0.057'
        ))
