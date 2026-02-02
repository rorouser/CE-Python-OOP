from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Bookmark, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass  # Registra Tag de forma sencilla

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'is_public', 'date_updated')
    list_editable = ('is_public',)
    list_filter = ('is_public', 'owner')
    search_fields = ('url', 'title', 'description')
    readonly_fields = ('date_created', 'date_updated')


