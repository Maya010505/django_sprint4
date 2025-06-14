from django.contrib import admin
from .models import Post, Location, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "pub_date", "author", "category", "is_published")
    list_filter = ("is_published", "category", "pub_date")
    search_fields = ("title", "text")
    date_hierarchy = "pub_date"
    ordering = ("-pub_date",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "is_published")
    list_filter = ("is_published",)
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published")
    list_filter = ("is_published",)
    search_fields = ("title", "description")
