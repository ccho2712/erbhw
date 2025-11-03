from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = '格式化 PostgreSQL 資料庫：刪除所有資料表與結構（需重新 migrate）'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('⚠️ 即將刪除所有 PostgreSQL 資料表與結構...'))

        with connection.cursor() as cursor:
            # 停用所有外鍵約束
            cursor.execute("SET session_replication_role = replica;")

            # 查詢所有 user-defined 資料表
            cursor.execute("""
                SELECT tablename FROM pg_tables
                WHERE schemaname = 'public';
            """)
            tables = cursor.fetchall()

            # 刪除所有資料表
            for table in tables:
                cursor.execute(f'DROP TABLE IF EXISTS "{table[0]}" CASCADE;')
                self.stdout.write(self.style.NOTICE(f'已刪除資料表：{table[0]}'))

            # 恢復外鍵約束
            cursor.execute("SET session_replication_role = DEFAULT;")

        self.stdout.write(self.style.SUCCESS('✅ PostgreSQL 資料庫已格式化（所有資料表與結構已刪除）'))
        self.stdout.write(self.style.WARNING('📌 請執行以下指令以重建資料庫：'))
        self.stdout.write(self.style.NOTICE('python manage.py makemigrations'))
        self.stdout.write(self.style.NOTICE('python manage.py migrate'))
        self.stdout.write(self.style.NOTICE('python manage.py createsuperuser'))
        self.stdout.write(self.style.NOTICE('python manage.py import_data'))

