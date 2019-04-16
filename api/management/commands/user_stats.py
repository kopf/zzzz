#!/usr/bin/env python3
import json

from django.core.management.base import BaseCommand

from api.models import User


class Command(BaseCommand):
    help = 'Print a dict of user status (number of users signed up per day) to stdout'

    def handle(self, *args, **options):
        stats = {}
        for user in User.objects.all():
            date_str = user.date_joined.strftime('%Y-%m-%d')
            stats.setdefault(date_str, 0)
            stats[date_str] += 1
        print(json.dumps(stats, indent=4))
