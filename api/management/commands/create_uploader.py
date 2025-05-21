from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = "Create an uploader user with an API token (no password login)"

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help="Uploader username")

    def handle(self, *args, **options):
        username = options['username']

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f"User '{username}' already exists"))
            return

        user = User(username=username)
        user.set_unusable_password()  # Prevent password-based login
        user.save()

        token, _ = Token.objects.get_or_create(user=user)

        self.stdout.write(self.style.SUCCESS("Uploader created"))
        self.stdout.write(f"Username: {username}")
        self.stdout.write(f"Token: {token.key}")
