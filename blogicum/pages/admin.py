from django.contrib import admin

from .models import Page


class PageAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)
    list_filter = ("title",)
    list_display_links = ("title",)
    empty_value_display = "Не задано"


admin.site.register(Page, PageAdmin)