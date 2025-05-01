from django.core.management.base import BaseCommand

from api.models import FlModel


class Command(BaseCommand):
    help = 'Seed database with initial FlModel data'

    def handle(self, *args, **options):
        data = [
            {"name": "Model A", "accuracy": 0.90, "precision": 0.88, "cross_validation": 0.85, "security": 0.95},
            {"name": "Model B", "accuracy": 0.85, "precision": 0.80, "cross_validation": 0.82, "security": 0.90},
            {"name": "Model C", "accuracy": 0.78, "precision": 0.75, "cross_validation": 0.70, "security": 0.88},
        ]

        for entry in data:
            FlModel.objects.update_or_create(name=entry["name"], defaults=entry)

        self.stdout.write(self.style.SUCCESS('Successfully seeded FlModel data.'))