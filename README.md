# erbhw
Django Data Workflow: Clean, Import, Export, Reset  

Step 1: Create the File
Open a text editor (Notepad, VS Code, Sublime Text, etc.).
Copy the full text below (the complete README content).
Paste it into the blank text file.
Save the file with the exact name: README.md (ensure "Save as type" is set to "All Files" to avoid .txt extension).
Step 2: Full README.md Content 

# ERB Homework: Django Data Management System

A Django application for managing book-related data with complete CSV import/export functionality, data cleaning, and database reset capabilities.

---

## 📋 Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Basic familiarity with command-line operations

---

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/ccho2712/erbhw.git
cd erbhw
2. Create & Activate Virtual Environment
bash
# Create virtual environment
python -m venv venv       # Windows
python3 -m venv venv      # macOS/Linux

# Activate virtual environment
venv\Scripts\activate     # Windows (Command Prompt)
source venv/bin/activate  # macOS/Linux (Terminal)
3. Install Dependencies
bash
pip install django
# If using requirements.txt:
# pip install -r requirements.txt
📂 Project Structure
plaintext
erbhw/
├── config/                 # Django project configuration
│   └── settings.py         # Core settings file
├── bookstore_app/          # Main application module
│   ├── models.py           # Data models (Book, Author, Publisher)
│   └── management/
│       └── commands/       # Custom management commands
│           ├── import_data.py  # CSV to database importer
│           ├── export_data.py  # Database to CSV exporter
│           └── clean_data.py   # Data cleaning utility
├── *.csv files             # Sample data files
└── manage.py               # Django command-line tool
🔄 Core Workflows
1. Database Migration
Create database tables from Django models:
bash
# Generate migration files
python manage.py makemigrations bookstore_app

# Apply migrations to create tables
python manage.py migrate
2. Import Data from CSV
Load data from CSV files into the database:
bash
python manage.py import_data
Requirements: CSV files (authors_export.csv, books_export.csv, publishers_export.csv) must exist in the root directory
Order: Authors → Publishers → Books (dependency handling)
3. Export Data to CSV
Save current database data to CSV files:
bash
python manage.py export_data
Overwrites existing CSV files with latest database data
Preserves model field structure in output files
4. Data Cleaning & Reset
Option 1: Delete All Data (Preserve Tables)
bash
python manage.py clean_data
Removes all records but keeps table structure intact
Option 2: Full Database Reset (No Tables remain)
bash
# WARNING: Deletes all data and resets auto-increment IDs
python manage.py reset_data

# Re-apply migrations if needed
python manage.py migrate
✅ Verification Methods
Check Data via Django Shell
bash
python manage.py shell
python
运行
# Example: Verify book records
from bookstore_app.models import Book
print(f"Total books in database: {Book.objects.count()}")

# Example: View first book details
if Book.objects.exists():
    print(Book.objects.first())
Access Admin Interface
Create a superuser account:
bash
python manage.py createsuperuser
Start the development server:
bash
python manage.py runserver
Visit http://127.0.0.1:8000/admin/ in your browser and log in to manage data.
🐛 Troubleshooting
Import Failures:
Ensure CSV column names match model field names (case-sensitive)
Check for duplicate unique fields (e.g., ISBN numbers)
Verify CSV files are in the project root directory
Migration Issues:
Delete db.sqlite3 and the bookstore_app/migrations/ folder (keep __init__.py)
Re-run makemigrations and migrate commands
Command Not Found:
Confirm virtual environment is activated
Check that custom commands exist in bookstore_app/management/commands/