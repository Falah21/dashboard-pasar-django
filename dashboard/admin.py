from django.contrib import admin
from .models import TagihanPasar

@admin.register(TagihanPasar)
class TagihanPasarAdmin(admin.ModelAdmin):
    list_display = (
        "id", "tgl_bayar", "nama_pasar", "stand", "pedagang",
        "nilai", "cabang", "jenis_tagihan", "tahun",
    )
    list_filter = ("cabang", "jenis_tagihan", "tahun")
    search_fields = ("nama_pasar", "pasar", "alamat", "stand", "pedagang", "sumber_file")
    ordering = ("-id",)
