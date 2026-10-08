import io
import pandas as pd
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from .models import TagihanPasar
from .utils.preprocessing import read_excel_file


class DashboardSmokeTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester",
            password="TestPass123!",
        )

    def test_dashboard_requires_login(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

    def test_excel_parser(self):
        frame = pd.DataFrame([{
            "Tgl Bayar": "15/01/2025",
            "Pasar": "Pasar Contoh",
            "Stand": "A01",
            "Pedagang": "Budi",
            "Periode": "Januari 2025",
            "Nilai": "Rp 125.000",
        }])
        buffer = io.BytesIO()
        frame.to_excel(buffer, index=False, engine="openpyxl")
        buffer.seek(0)

        uploaded = SimpleUploadedFile(
            "100 A 2020-2025.xlsx",
            buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        rows = read_excel_file(uploaded)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["cabang"], "Selatan")
        self.assertEqual(rows[0]["jenis_tagihan"], "Air")
        self.assertEqual(rows[0]["nilai"], 125000)

    def test_dashboard_after_login(self):
        TagihanPasar.objects.create(
            nama_pasar="Pasar Contoh",
            stand="A01",
            pedagang="Budi",
            nilai=125000,
            cabang="Selatan",
            jenis_tagihan="Air",
            tahun=2025,
            bulan=1,
            tahun_bulan="2025-01",
        )
        self.client.login(username="tester", password="TestPass123!")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pasar Contoh")
