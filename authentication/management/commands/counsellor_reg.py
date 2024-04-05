from django.core.management.base import BaseCommand
from authentication.models import CustomUser

class Command(BaseCommand):
    help = 'Create a counselor user'

    def handle(self, *args, **options):
        counselor_username = input('Enter counselor username: ')
        counselor_password = input('Enter counselor password: ')

        counselor = CustomUser.objects.create_user(username=counselor_username, password=counselor_password, role=CustomUser.COUNSELOR)
        self.stdout.write(self.style.SUCCESS(f'Counselor user "{counselor_username}" created successfully.'))
