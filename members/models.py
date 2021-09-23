from django.db import models
from django.contrib.auth.backends import ModelBackend
from affiliate.models import NewUser
class EmailAuthBackend(ModelBackend):
    """
    Email Authentication Backend

    Allows a user to sign in using an email/password pair rather than
    a username/password pair.
    """

    def authenticate(self, request, email=None, password=None, **kwargs):
        """ Authenticate a user based on email address as the user name. """
        try:
            user = NewUser.objects.get(email=email)
        except NewUser.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            NewUser().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user