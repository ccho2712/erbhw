import csv
from django.core.management.base import BaseCommand
from bookstore_app.models import Author, Book, Publisher

class Command(BaseCommand):
    help = '匯出資料到 CSV'

    def handle(self, *args, **kwargs):
        with open('authors_export.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'birth_date'])
            for author in Author.objects.all():
                writer.writerow([author.name, author.birth_date])

        with open('publishers_export.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'city'])
            for publisher in Publisher.objects.all():
                writer.writerow([publisher.name, publisher.city])

        with open('books_export.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['title', 'publication_date', 'author_name', 'publisher_name'])
            for book in Book.objects.all():
                writer.writerow([book.title, book.publication_date, book.author.name, book.publisher.name])

        self.stdout.write(self.style.SUCCESS('資料匯出完成'))
