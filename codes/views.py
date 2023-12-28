from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect

from .models import UniqueGiftCode
from .forms import UploadExcelForm

import openpyxl


@user_passes_test(lambda u: u.is_superuser)
def upload_unique_gift_codes_view(request):
    if request.method == "GET":
        return render(request, "admin/upload_gift_codes_excel.html", {"form": UploadExcelForm()})

    excel_file = request.FILES["excel_file"]
    wb = openpyxl.load_workbook(excel_file)
    ws = wb.active

    for row in ws.iter_rows(min_row=2, values_only=True):
        value, gift_type = row[0:2]
        if not UniqueGiftCode.objects.filter(code=value).exists():
            UniqueGiftCode.objects.create(code=value, gift_type=gift_type)

    return redirect("/admin/codes/uniquegiftcode/")
