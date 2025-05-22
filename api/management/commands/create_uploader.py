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

        print("Uploader created", flush=True)
        print(f"Username: {username}", flush=True)

        with open("/tmp/uploader_token.txt", "w") as f:
            f.write(token.key)

        self.stdout.write(self.style.SUCCESS("Wrote token to /tmp/uploader_token.txt"))

        print(f"Token: {token.key}", flush=True)
