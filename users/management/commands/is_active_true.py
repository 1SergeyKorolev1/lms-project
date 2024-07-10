from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        users = User.objects.all()
        if users:
            for user in users:
                user.is_active = True
                user.save()