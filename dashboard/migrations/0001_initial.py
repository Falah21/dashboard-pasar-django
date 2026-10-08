from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TagihanPasar",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tgl_bayar", models.DateField(blank=True, null=True)),
                ("tgl_closing", models.DateField(blank=True, null=True)),
                ("pasar", models.CharField(blank=True, default="", max_length=255)),
                ("nama_pasar", models.CharField(blank=True, default="", max_length=255)),
                ("alamat", models.TextField(blank=True, default="")),
                ("stand", models.CharField(blank=True, default="", max_length=255)),
                ("pedagang", models.CharField(blank=True, default="", max_length=255)),
                ("periode", models.CharField(blank=True, default="", max_length=255)),
                ("nilai", models.DecimalField(decimal_places=2, default=0, max_digits=18)),
                ("kode_cabang", models.CharField(blank=True, default="", max_length=50)),
                ("cabang", models.CharField(blank=True, default="", max_length=100)),
                ("jenis_tagihan", models.CharField(blank=True, default="", max_length=100)),
                ("sumber_file", models.CharField(blank=True, default="", max_length=500)),
                ("tahun", models.PositiveIntegerField(blank=True, null=True)),
                ("bulan", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("tahun_bulan", models.CharField(blank=True, default="", max_length=7)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "tagihan_pasar",
                "ordering": ["-id"],
            },
        ),
        migrations.AddIndex(
            model_name="tagihanpasar",
            index=models.Index(fields=["tahun"], name="tagihan_pas_tahun_819845_idx"),
        ),
        migrations.AddIndex(
            model_name="tagihanpasar",
            index=models.Index(fields=["cabang"], name="tagihan_pas_cabang_a4cc3f_idx"),
        ),
        migrations.AddIndex(
            model_name="tagihanpasar",
            index=models.Index(fields=["jenis_tagihan"], name="tagihan_pas_jenis_t_9ee74b_idx"),
        ),
        migrations.AddIndex(
            model_name="tagihanpasar",
            index=models.Index(fields=["nama_pasar"], name="tagihan_pas_nama_pa_eedacb_idx"),
        ),
        migrations.AddIndex(
            model_name="tagihanpasar",
            index=models.Index(fields=["sumber_file"], name="tagihan_pas_sumber__9efa76_idx"),
        ),
    ]
