from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework_simplejwt.tokens import RefreshToken

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_jwt_token(sender, instance=None, created=False, **kwargs):
    if created:
        RefreshToken.for_user(instance)
      