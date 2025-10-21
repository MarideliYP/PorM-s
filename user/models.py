from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=5, blank=True, null=True)
    code_expiration = models.DateTimeField(blank=True, null=True)
    failed_attempts = models.PositiveIntegerField(default=0)
    code_blocked_until = models.DateTimeField(blank=True, null=True)
    dir = models.CharField(default='Provincia, Municipio, calle/calles no.', max_length=200)
    image = models.ImageField(upload_to='img/', default='img/user.png')

    def is_code_valid(self, entered_code):
        now = timezone.now()
        if self.code_blocked_until and now < self.code_blocked_until:
            return False
        return self.verification_code == entered_code and self.code_expiration and self.code_expiration > now
