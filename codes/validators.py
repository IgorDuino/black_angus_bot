import os
from django.core.exceptions import ValidationError


def validate_file_extension(valid_extensions):
    def _validate_file_extension(value):
        ext = os.path.splitext(value.name)[1]
        if not ext.lower() in valid_extensions:
            raise ValidationError(f"File extension must be {valid_extensions}")

    return _validate_file_extension
