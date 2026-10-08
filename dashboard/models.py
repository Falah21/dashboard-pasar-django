from django.db import models


class TagihanPasar(models.Model):
    tgl_bayar = models.DateField(null=True, blank=True)
    tgl_closing = models.DateField(null=True, blank=True)
    pasar = models.CharField(max_length=255, blank=True, default="")
    nama_pasar = models.CharField(max_length=255, blank=True, default="")
    alamat = models.TextField(blank=True, default="")
    stand = models.CharField(max_length=255, blank=True, default="")
    pedagang = models.CharField(max_length=255, blank=True, default="")
    periode = models.CharField(max_length=255, blank=True, default="")
    nilai = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    kode_cabang = models.CharField(max_length=50, blank=True, default="")
    cabang = models.CharField(max_length=100, blank=True, default="")
    jenis_tagihan = models.CharField(max_length=100, blank=True, default="")
    sumber_file = models.CharField(max_length=500, blank=True, default="")
    tahun = models.PositiveIntegerField(null=True, blank=True)
    bulan = models.PositiveSmallIntegerField(null=True, blank=True)
    tahun_bulan = models.CharField(max_length=7, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tagihan_pasar"
        ordering = ["-id"]
        indexes = [
            models.Index(fields=["tahun"]),
            models.Index(fields=["cabang"]),
            models.Index(fields=["jenis_tagihan"]),
            models.Index(fields=["nama_pasar"]),
            models.Index(fields=["sumber_file"]),
        ]

    def __str__(self):
        return f"{self.nama_pasar or self.pasar} - {self.stand}"
