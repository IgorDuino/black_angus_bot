from django import forms
from .validators import validate_file_extension


class UploadExcelForm(forms.Form):
    excel_file = forms.FileField(
        required=True,
        allow_empty_file=False,
        label="Excel file",
        validators=[validate_file_extension([".xlsx"])],
    )
