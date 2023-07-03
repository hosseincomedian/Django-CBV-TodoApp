from django.core.management.base import BaseCommand
from faker import Faker
import random
from accounts.models import User
from todo.models import Todo


class Command(BaseCommand):
    help = "fake data for testing"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        user = User.objects.create_user(
            email=self.fake.email(),
            password="test123456",
        )
        for _ in range(5):
            Todo.objects.create(
                user=user,
                title=self.fake.paragraph(nb_sentences=1),
                complete=random.choice([True, False]),
            )
