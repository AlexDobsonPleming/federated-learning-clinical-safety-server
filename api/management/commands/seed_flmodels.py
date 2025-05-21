from django.core.management.base import BaseCommand
from api.models import FlModel, LocalModel
import random

class Command(BaseCommand):
    help = 'Seed database: one FlModel and 5 LocalModel entries with NHS Trust sources'

    def handle(self, *args, **options):
        LocalModel.objects.all().delete()
        FlModel.objects.all().delete()

        fl = FlModel.objects.create(
            name='Swangeese with Transfer Learning Model',
            accuracy=0.69,
            generalisability=0.057,
            security=None,
        )

        nhs_trusts = [
            'Barts Health NHS Trust',
            'Cambridge University Hospitals NHS Foundation Trust',
            'Guy’s and St Thomas’ NHS Foundation Trust',
            'Oxford University Hospitals NHS Foundation Trust',
            'University Hospitals Birmingham NHS Foundation Trust',
            'King’s College Hospital NHS Foundation Trust',
            'Manchester University NHS Foundation Trust',
        ]

        for i in range(1, 6):
            LocalModel.objects.create(
                fl_model=fl,
                name=f'Local Model {i}',
                relatability=round(random.uniform(0.0, 1.0), 3),
                source=random.choice(nhs_trusts),
            )

        self.stdout.write(self.style.SUCCESS(
            'Database seeded: 1 FlModel + 5 LocalModel entries with NHS Trust sources'
        ))
