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


        epsilon_3_model = FlModel.objects.create(
            name='Epsilon 3 Model',
            accuracy=0.3686,
            generalisability=0.0540,
            privacy=1,
            leakage_chance=1 * (10 **-5),
        )

        # Create 2 local models based on shubham's run
        LocalModel.objects.create(
            fl_model=epsilon_3_model,
            name='Site 1',
            privacy=0.8811,
            leakage_chance=1 * (10 **-5),
            noise=0.1358,
        )

        LocalModel.objects.create(
            fl_model=epsilon_3_model,
            name=f'Site 2',
            privacy=0.8811,
            leakage_chance=1 * (10 ** -5),
            noise=0.2037,
        )

        epsilon_5_model = FlModel.objects.create(
            name='Epsilon 5 Model',
            accuracy=0.3671,
            generalisability=0.0751,
            privacy=5,
            leakage_chance=1 * (10 **-5),
        )

        LocalModel.objects.create(
            fl_model=epsilon_5_model,
            name='Site 1',
            privacy=1.5045,
            leakage_chance=1 * (10 ** -5),
            noise=0.0815,
        )

        LocalModel.objects.create(
            fl_model=epsilon_5_model,
            name=f'Site 2',
            privacy=1.5045,
            leakage_chance=1 * (10 ** -5),
            noise=0.1222,
        )

        epsilon_10_model = FlModel.objects.create(
            name='Epsilon 10 Model',
            accuracy=0.3882,
            generalisability=0.0429,
            privacy=10,
            leakage_chance=1 * (10 **-5),
        )

        LocalModel.objects.create(
            fl_model=epsilon_10_model,
            name='Site 1',
            privacy=3.1945,
            leakage_chance=1 * (10 ** -5),
            noise=0.0407,
        )

        LocalModel.objects.create(
            fl_model=epsilon_10_model,
            name=f'Site 2',
            privacy=3.1943,
            leakage_chance=1 * (10 ** -5),
            noise=0.0611,
        )

        epsilon_15_model = FlModel.objects.create(
            name='Epsilon 15 Model',
            accuracy=0.4033,
            generalisability=0.0386,
            privacy=15,
            leakage_chance=1 * (10 **-5),
        )

        LocalModel.objects.create(
            fl_model=epsilon_15_model,
            name='Site 1',
            privacy=5.0812,
            leakage_chance=1 * (10 ** -5),
            noise=0.0272,
        )

        LocalModel.objects.create(
            fl_model=epsilon_15_model,
            name=f'Site 2',
            privacy=5.0812,
            leakage_chance=1 * (10 ** -5),
            noise=0.0407,
        )

        self.stdout.write(self.style.SUCCESS(
            'Database seeded models'
        ))
