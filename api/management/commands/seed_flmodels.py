# api/management/commands/seed.py
from django.core.management.base import BaseCommand
from api.models import FlModel, LocalModel
import random

class Command(BaseCommand):
    help = 'Seed database: one FlModel and 5 LocalModel entries as Site 1–5'

    def handle(self, *args, **options):
        # Clear out existing data
        LocalModel.objects.all().delete()
        FlModel.objects.all().delete()

        # Create the global FL model
        fl = FlModel.objects.create(
            name='Swangeese with Transfer Learning Model',
            accuracy=0.69,
            generalisability=0.057,
            privacy=None,
        )

        # Create 5 local models named Site 1–5 with random metrics
        for i in range(1, 6):
            LocalModel.objects.create(
                fl_model=fl,
                name=f'Site {i}',
                privacy=round(random.uniform(0.0, 1.0), 3),
                leakage_chance=round(random.uniform(0.0, 1.0), 3),
                noise=round(random.uniform(0.0, 1.0), 3),
            )

        self.stdout.write(self.style.SUCCESS(
            'Database seeded: 1 FlModel + 5 LocalModel entries (Site 1 - 5)'
        ))
