from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch.dispatcher import receiver


class User(AbstractUser):
    token = models.CharField(
        max_length=36, unique=True, blank=True, default=uuid4)
    user_class = models.IntegerField(blank=True, default=0)


class Subdomain(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=128, unique=True)
    ip = models.CharField(max_length=15, unique=False, null=True)
    ipv6 = models.CharField(max_length=45, unique=False, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)


@receiver(models.signals.pre_delete, sender=Subdomain)
def subdomain_delete(sender, instance, **kwargs):
    from api.dns import delete_dns_records
    delete_dns_records(instance.name)
