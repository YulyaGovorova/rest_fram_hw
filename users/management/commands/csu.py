from django.core.management import BaseCommand

from users.models import User



class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin3@sky.pro',
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )

        user.set_password('admin_password')
        user.save()