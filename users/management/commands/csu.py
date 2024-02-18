from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Суперюзер
    """

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin3@sky.pro',
            name='admin3',
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )

        user.set_password('12345')
        user.save()