from django.contrib import admin

from .models import Code, UniqueCode


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = ("phrase", "is_active", "max_uses", "uses")
    list_filter = ("is_active", "max_uses")
    search_fields = ("phrase",)


@admin.register(UniqueCode)
class UniqueCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "phrase_code", "used")
    list_filter = ("used",)
    search_fields = ("code", "phrase_code__phrase")
