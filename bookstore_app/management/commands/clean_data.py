from django.core.management.base import BaseCommand
from bookstore_app.models import Author, Book, Publisher

class Command(BaseCommand):
    help = '清除所有資料'

    def handle(self, *args, **kwargs):
        Book.objects.all().delete()
        Author.objects.all().delete()
        Publisher.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('已清除所有資料'))
