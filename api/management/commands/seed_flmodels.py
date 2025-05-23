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
        swangeese = FlModel.objects.create(
            name='Swangeese with Transfer Learning Model',
            accuracy=0.69,
            generalisability=0.057,
            privacy=None,
            leakage_chance=None
        )

        epsilon_1_model = FlModel.objects.create(
            name='Epsilon 1 Model',
            accuracy=None,
            generalisability=None,
            privacy=1,
            leakage_chance=1 * (10 **-5),
        )

        # Create 2 local models based on shubham's run
        LocalModel.objects.create(
            fl_model=epsilon_1_model,
            name='Site 1',
            privacy=0.0083,
            leakage_chance=1 * (10 **-5),
            noise=0.4073,
        )

        LocalModel.objects.create(
            fl_model=epsilon_1_model,
            name=f'Site 2',
            privacy=0.0083,
            leakage_chance=1 * (10 ** -5),
            noise=0.6112,
        )

        epsilon_5_model = FlModel.objects.create(
            name='Epsilon 5 Model',
            accuracy=None,
            generalisability=None,
            privacy=5,
            leakage_chance=1 * (10 **-5),
        )

        LocalModel.objects.create(
            fl_model=epsilon_5_model,
            name='Site 1',
            privacy=0.0417,
            leakage_chance=1 * (10 ** -5),
            noise=0.0815,
        )

        LocalModel.objects.create(
            fl_model=epsilon_5_model,
            name=f'Site 2',
            privacy=0.0417,
            leakage_chance=1 * (10 ** -5),
            noise=0.1222,
        )

        epsilon_10_model = FlModel.objects.create(
            name='Epsilon 10 Model',
            accuracy=None,
            generalisability=None,
            privacy=10,
            leakage_chance=1 * (10 **-5),
        )

        LocalModel.objects.create(
            fl_model=epsilon_10_model,
            name='Site 1',
            privacy=0.0834,
            leakage_chance=1 * (10 ** -5),
            noise=0.0407,
        )

        LocalModel.objects.create(
            fl_model=epsilon_10_model,
            name=f'Site 2',
            privacy=0.0834,
            leakage_chance=1 * (10 ** -5),
            noise=0.0611,
        )

        epsilon_15_model = FlModel.objects.create(
            name='Epsilon 15 Model',
            accuracy=None,
            generalisability=None,
            privacy=15,
            leakage_chance=1 * (10 **-5),
        )

        LocalModel.objects.create(
            fl_model=epsilon_15_model,
            name='Site 1',
            privacy=0.1252,
            leakage_chance=1 * (10 ** -5),
            noise=0.0272,
        )

        LocalModel.objects.create(
            fl_model=epsilon_15_model,
            name=f'Site 2',
            privacy=0.1252,
            leakage_chance=1 * (10 ** -5),
            noise=0.0407,
        )

        self.stdout.write(self.style.SUCCESS(
            'Database seeded: 1 FlModel + 2 LocalModel entries'
        ))
