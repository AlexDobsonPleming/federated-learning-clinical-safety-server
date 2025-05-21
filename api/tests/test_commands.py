import io
import pytest

from django.core.management import call_command
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

@pytest.mark.django_db
class TestCreateUploaderCommand:

    def test_creates_user_and_token(self, capsys):
        """
        Running `create_uploader alice` should:
         - create a User(username='alice') with unusable password
         - create a Token tied to that user
         - output SUCCESS and echo username + token
        """
        out = io.StringIO()
        call_command('create_uploader', 'alice', stdout=out)

        output = out.getvalue()
        # User created
        user = User.objects.get(username='alice')
        assert not user.has_usable_password()

        # Token created
        token = Token.objects.get(user=user)
        assert token.key in output
        assert "Uploader created" in output
        assert "Username: alice" in output

    def test_already_exists(self):
        """
        Running the command a second time with same username should:
         - not create another user or token
         - print an ERROR about existing user
        """
        # First invocation
        call_command('create_uploader', 'bob')

        # Capture second invocation
        out = io.StringIO()
        call_command('create_uploader', 'bob', stdout=out)

        output = out.getvalue()
        # It should mention that user already exists
        assert "already exists" in output.lower()

        # Only one user and one token remain
        assert User.objects.filter(username='bob').count() == 1
        assert Token.objects.filter(user__username='bob').count() == 1
