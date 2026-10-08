from django import forms
from django.conf import settings


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        single = super().clean
        if not isinstance(data, (list, tuple)):
            data = [data] if data else []
        return [single(item, initial) for item in data]


class UploadForm(forms.Form):
    files = MultipleFileField(required=True, label="File Excel")
    replace_all = forms.BooleanField(
        required=False,
        label="Hapus seluruh data lama sebelum import",
    )

    def clean_files(self):
        files = self.files.getlist("files")
        if not files:
            raise forms.ValidationError("Pilih minimal satu file Excel.")

        max_bytes = getattr(settings, "MAX_UPLOAD_SIZE_MB", 50) * 1024 * 1024
        for file_obj in files:
            if not file_obj.name.lower().endswith((".xlsx", ".xls")):
                raise forms.ValidationError(
                    f"'{file_obj.name}' bukan file Excel (.xlsx/.xls)."
                )
            if file_obj.size > max_bytes:
                raise forms.ValidationError(
                    f"'{file_obj.name}' melebihi batas {max_bytes // (1024 * 1024)} MB."
                )
        return files
