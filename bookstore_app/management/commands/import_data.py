import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from django.core.management import call_command
from bookstore_app.models import Author, Book, Publisher

class Command(BaseCommand):
    help = '執行 migrate 並匯入 CSV 資料到 Django 資料庫'

    def handle(self, *args, **kwargs):
        # Step 1: 執行 migrate
        self.stdout.write(self.style.WARNING('📦 執行 makemigrations 和 migrate...'))
        try:
            call_command('makemigrations', 'bookstore_app')
            call_command('migrate')
            self.stdout.write(self.style.SUCCESS('✅ 資料表結構已更新'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ migrate 發生錯誤：{e}'))
            return

        # Step 2: 匯入 Publisher
        try:
            with open('bookstore_app/fixtures/publishers.csv', newline='', encoding='utf-8') as f:
                for row in csv.DictReader(f):
                    name = row['name'].strip()
                    city = row['city'].strip()
                    Publisher.objects.get_or_create(name=name, city=city)
            self.stdout.write(self.style.SUCCESS('Publisher 匯入完成'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Publisher 匯入錯誤：{e}'))

        # Step 3: 匯入 Author
        try:
            with open('bookstore_app/fixtures/authors.csv', newline='', encoding='utf-8') as f:
                for row in csv.DictReader(f):
                    name = row['name'].strip()
                    birth_date = row['birth_date'].strip()
                    try:
                        birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d').date()
                    except ValueError:
                        self.stdout.write(self.style.WARNING(f'跳過作者 {name}，日期格式錯誤：{birth_date}'))
                        continue
                    Author.objects.get_or_create(name=name, birth_date=birth_date_obj)
            self.stdout.write(self.style.SUCCESS('Author 匯入完成'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Author 匯入錯誤：{e}'))

        # Step 4: 匯入 Book
        try:
            with open('bookstore_app/fixtures/books.csv', newline='', encoding='utf-8') as f:
                for row in csv.DictReader(f):
                    title = row['title'].strip()
                    pub_date = row['publication_date'].strip()
                    author_name = row['author_name'].strip()
                    publisher_name = row['publisher_name'].strip()

                    try:
                        pub_date_obj = datetime.strptime(pub_date, '%Y-%m-%d').date()
                    except ValueError:
                        self.stdout.write(self.style.WARNING(f'跳過書籍 {title}，日期格式錯誤：{pub_date}'))
                        continue

                    try:
                        author = Author.objects.get(name=author_name)
                    except Author.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'跳過書籍 {title}，找不到作者：{author_name}'))
                        continue

                    try:
                        publisher = Publisher.objects.get(name=publisher_name)
                    except Publisher.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'跳過書籍 {title}，找不到出版社：{publisher_name}'))
                        continue

                    Book.objects.get_or_create(
                        title=title,
                        publication_date=pub_date_obj,
                        author=author,
                        publisher=publisher
                    )
            self.stdout.write(self.style.SUCCESS('Book 匯入完成'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Book 匯入錯誤：{e}'))

        self.stdout.write(self.style.SUCCESS('🎉 所有資料匯入完成'))

