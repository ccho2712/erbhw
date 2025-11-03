# Register your models here.
from django.contrib import admin
from .models import Author, Book, Publisher
from django.db import models

@admin.register(Book)
class BookstoreAdmin(admin.ModelAdmin):
    list_display = ('title', 'publication_date', 'author', 'publisher')
    search_fields = ('title', 'author__name', 'publisher__name')
    list_filter = ('publication_date', 'publisher')
    ordering = ('publication_date',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date')

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
