from django.contrib import admin
import openpyxl
from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from django.urls import path
from django.contrib import messages
from django.shortcuts import redirect

from .models import Code, UniqueCode


class UploadExcelForm(forms.Form):
    excel_file = forms.FileField()


def upload_unique_codes(modeladmin, request, queryset=None):
    if not (queryset is None):
        if len(queryset) != 1:
            modeladmin.message_user(request, "Please select only one Code for importing!", level=messages.ERROR)
            return

        selected_code = queryset[0]
        return render(request, "admin/upload_excel.html", {"form": UploadExcelForm(), "selected_code": selected_code})


upload_unique_codes.short_description = "Загрузить уникальные коды из Excel"


def upload_unique_codes_view(request):
    excel_file = request.FILES["excel_file"]
    wb = openpyxl.load_workbook(excel_file)
    ws = wb.active

    code_id = request.POST["code_id"]
    code = Code.objects.get(id=code_id)

    for row in ws.iter_rows(min_row=2, values_only=True):
        unique_code_value = row[0]
        if not UniqueCode.objects.filter(code=unique_code_value).exists():
            UniqueCode.objects.create(phrase_code=code, code=unique_code_value)

    return redirect("/admin/codes/uniquecode/")


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = ("phrase", "is_active", "max_uses", "uses")
    list_filter = ("is_active", "max_uses")
    search_fields = ("phrase",)
    actions = [upload_unique_codes]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-to-unique-codes/",
                self.admin_site.admin_view(upload_unique_codes_view),
                name="import_to_unique_codes",
            ),
        ]
        return custom_urls + urls


@admin.register(UniqueCode)
class UniqueCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "phrase_code", "used")
    list_filter = ("used",)
    search_fields = ("code", "phrase_code__phrase")
