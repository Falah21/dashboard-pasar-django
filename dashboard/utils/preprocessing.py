# # import re
# # from datetime import datetime
# # from decimal import Decimal, InvalidOperation

# # import pandas as pd

# # from dashboard.models import TagihanPasar


# # KODE_CABANG = {
# #     "100": "Selatan",
# #     "200": "Timur",
# #     "300": "Utara",
# # }

# # KODE_JENIS = {
# #     "A": "Air",
# #     "L": "Listrik",
# #     "T": "Tempat",
# # }

# # ALIASES = {
# #     "tgl bayar": "tgl_bayar",
# #     "tanggal bayar": "tgl_bayar",
# #     "tgl pembayaran": "tgl_bayar",
# #     "tanggal pembayaran": "tgl_bayar",
# #     "tgl closing": "tgl_closing",
# #     "tanggal closing": "tgl_closing",
# #     "pasar": "pasar",
# #     "nama pasar": "nama_pasar",
# #     "alamat": "alamat",
# #     "stand": "stand",
# #     "pedagang": "pedagang",
# #     "nama pedagang": "pedagang",
# #     "periode": "periode",
# #     "nilai": "nilai",
# #     "nilai tagihan": "nilai",
# #     "nominal": "nilai",
# #     "kode cabang": "kode_cabang",
# #     "cabang": "cabang",
# #     "jenis tagihan": "jenis_tagihan",
# #     "jenis": "jenis_tagihan",
# # }


# # def normalize_header(value):
# #     text = str(value).strip().lower()
# #     text = re.sub(r"[_\-]+", " ", text)
# #     text = re.sub(r"\s+", " ", text)
# #     return text


# # def parse_filename(filename):
# #     stem = filename.rsplit("/", 1)[-1]
# #     stem = re.sub(r"\.(xlsx|xls)$", "", stem, flags=re.I).strip()
# #     match = re.match(r"^(\d+)\s+([ALT])(?:\s+(.*))?$", stem, flags=re.I)
# #     if not match:
# #         raise ValueError(
# #             f"Nama file '{filename}' tidak sesuai. Gunakan contoh: "
# #             "'100 A 2020-2025.xlsx'."
# #         )

# #     kode = match.group(1)
# #     jenis_kode = match.group(2).upper()
# #     periode = (match.group(3) or "").strip()
# #     return {
# #         "kode_cabang": kode,
# #         "cabang": KODE_CABANG.get(kode, kode),
# #         "jenis_tagihan": KODE_JENIS.get(jenis_kode, jenis_kode),
# #         "periode_filename": periode,
# #     }


# # def _clean_text(value):
# #     if pd.isna(value):
# #         return ""
# #     return str(value).strip()


# # def _clean_decimal(value):
# #     if pd.isna(value) or value == "":
# #         return Decimal("0")
# #     if isinstance(value, (int, float)):
# #         return Decimal(str(value))
# #     text = str(value).strip().replace("Rp", "").replace("rp", "").replace(" ", "")
# #     # Handle Indonesian formats such as 1.234.567,89 and plain 1234567.89.
# #     if "," in text and "." in text:
# #         if text.rfind(",") > text.rfind("."):
# #             text = text.replace(".", "").replace(",", ".")
# #         else:
# #             text = text.replace(",", "")
# #     elif "," in text:
# #         text = text.replace(".", "").replace(",", ".")
# #     else:
# #         # Indonesian currency commonly uses dots as thousands separators:
# #         # 125.000 -> 125000, while 125.50 is kept as a decimal.
# #         parts = text.split(".")
# #         if len(parts) > 1:
# #             if all(part.isdigit() for part in parts) and len(parts[-1]) == 3:
# #                 text = "".join(parts)
# #             elif len(parts) > 2:
# #                 text = "".join(parts)
# #     try:
# #         return Decimal(text or "0")
# #     except (InvalidOperation, ValueError):
# #         return Decimal("0")


# # def _to_date(value):
# #     if pd.isna(value) or value == "":
# #         return None
# #     parsed = pd.to_datetime(value, errors="coerce", dayfirst=True)
# #     if pd.isna(parsed):
# #         return None
# #     return parsed.date()


# # def _derive_year_month(row, filename_info):
# #     for key in ("tgl_bayar", "tgl_closing"):
# #         date_value = row.get(key)
# #         if date_value:
# #             return date_value.year, date_value.month

# #     years = re.findall(r"(?:19|20)\d{2}", filename_info.get("periode_filename", ""))
# #     if years:
# #         return int(years[0]), None

# #     period = _clean_text(row.get("periode", ""))
# #     years = re.findall(r"(?:19|20)\d{2}", period)
# #     if years:
# #         return int(years[0]), None

# #     return None, None


# # def read_excel_file(file_obj):
# #     info = parse_filename(file_obj.name)
# #     try:
# #         workbook = pd.read_excel(file_obj, sheet_name=0)
# #     except Exception as exc:
# #         raise ValueError(f"Gagal membaca '{file_obj.name}': {exc}") from exc

# #     if workbook.empty:
# #         raise ValueError(f"'{file_obj.name}' tidak memiliki data.")

# #     renamed = {}
# #     for column in workbook.columns:
# #         key = normalize_header(column)
# #         if key in ALIASES:
# #             renamed[column] = ALIASES[key]
# #     workbook = workbook.rename(columns=renamed)

# #     # Some files use the code/metadata only in the filename. Missing columns
# #     # are therefore allowed and filled safely.
# #     for column in ALIASES.values():
# #         if column not in workbook.columns:
# #             workbook[column] = ""

# #     rows = []
# #     for _, raw in workbook.iterrows():
# #         row = {column: raw.get(column, "") for column in ALIASES.values()}
# #         tgl_bayar = _to_date(row["tgl_bayar"])
# #         tgl_closing = _to_date(row["tgl_closing"])
# #         row["tgl_bayar"] = tgl_bayar
# #         row["tgl_closing"] = tgl_closing

# #         row["kode_cabang"] = _clean_text(row["kode_cabang"]) or info["kode_cabang"]
# #         row["cabang"] = _clean_text(row["cabang"]) or info["cabang"]
# #         row["jenis_tagihan"] = _clean_text(row["jenis_tagihan"]) or info["jenis_tagihan"]

# #         row["pasar"] = _clean_text(row["pasar"])
# #         row["nama_pasar"] = _clean_text(row["nama_pasar"]) or row["pasar"]
# #         row["alamat"] = _clean_text(row["alamat"])
# #         row["stand"] = _clean_text(row["stand"])
# #         row["pedagang"] = _clean_text(row["pedagang"])
# #         row["periode"] = _clean_text(row["periode"]) or info["periode_filename"]
# #         row["nilai"] = _clean_decimal(row["nilai"])
# #         row["sumber_file"] = file_obj.name

# #         year, month = _derive_year_month(row, info)
# #         row["tahun"] = year
# #         row["bulan"] = month
# #         row["tahun_bulan"] = f"{year:04d}-{month:02d}" if year and month else (
# #             f"{year:04d}" if year else ""
# #         )

# #         # Skip completely blank records.
# #         meaningful = any([
# #             row["nama_pasar"], row["stand"], row["pedagang"],
# #             row["periode"], row["nilai"] != 0,
# #         ])
# #         if meaningful:
# #             rows.append(row)

# #     return rows


# # def preprocess_files(files):
# #     rows = []
# #     errors = []
# #     successful_files = []

# #     for file_obj in files:
# #         try:
# #             file_rows = read_excel_file(file_obj)
# #             if not file_rows:
# #                 raise ValueError("Tidak ada baris data yang dapat diproses.")
# #             rows.extend(file_rows)
# #             successful_files.append(file_obj.name)
# #         except Exception as exc:
# #             errors.append(str(exc))

# #     return rows, errors, successful_files


# # def save_rows(rows, replace_all=False):
# #     if not rows:
# #         return 0

# #     if replace_all:
# #         TagihanPasar.objects.all().delete()

# #     existing = set(
# #         TagihanPasar.objects.values_list("sumber_file", flat=True).distinct()
# #     )
# #     seen_files = set()
# #     new_rows = []
# #     for row in rows:
# #         source = row["sumber_file"]
# #         if source in existing or source in seen_files:
# #             continue
# #         seen_files.add(source)
# #         new_rows.append(row)

# #     if not new_rows:
# #         return 0

# #     objects = [TagihanPasar(**row) for row in new_rows]
# #     TagihanPasar.objects.bulk_create(objects, batch_size=1000)
# #     return len(objects)


# # def get_existing_files():
# #     return list(
# #         TagihanPasar.objects.values_list("sumber_file", flat=True)
# #         .distinct()
# #         .order_by("sumber_file")
# #     )

# import re
# from datetime import datetime
# from decimal import Decimal, InvalidOperation

# import pandas as pd

# from dashboard.models import TagihanPasar


# # =========================================================
# # KONFIGURASI TAHUN (sama seperti Streamlit)
# # =========================================================
# TAHUN_MINIMAL = 2010
# TAHUN_MAKSIMAL = datetime.now().year + 1


# # =========================================================
# # MAPPING (tidak berubah)
# # =========================================================
# KODE_CABANG = {
#     "100": "Selatan",
#     "200": "Timur",
#     "300": "Utara",
# }

# KODE_JENIS = {
#     "A": "Air",
#     "L": "Listrik",
#     "T": "Tempat",
# }

# # ⭐ TAMBAHAN: Mapping kode pasar → nama pasar (sama seperti Streamlit)
# KODE_PASAR = {
#     "101": "BENDUL MERISI",
#     "102": "GAYUNG SARI",
#     "103": "WONOKROMO LAMA",
#     "104": "DUKUH KUPANG",
#     "105": "DUKUH KUPANG BARAT",
#     "106": "GENTENG BARU",
#     "107": "KARANG PILANG",
#     "108": "LAKARSANTRI",
#     "109": "BANGKINGAN",
#     "110": "HWN KARANG PILANG",
#     "111": "KEMBANG",
#     "112": "KEDUNGSARI",
#     "113": "KEDUNGDORO",
#     "114": "KUPANG",
#     "115": "PANDEGILING",
#     "116": "KUPANG GUNUNG",
#     "117": "PAKIS",
#     "118": "WONOKITRI",
#     "119": "TUNJUNGAN",
#     "120": "WONOKROMO",
#     "201": "BUNGA BRATANG",
#     "202": "BURUNG BRATANG",
#     "203": "INPRES BRATANG",
#     "204": "KEPUTIH",
#     "205": "GUBENG MASJID",
#     "206": "GUBENG KERTAJAYA",
#     "207": "KAPASAN",
#     "208": "ASWOTOMO",
#     "209": "KERTOPATEN",
#     "210": "KENDANGSARI",
#     "211": "TENGGILIS",
#     "212": "PANJANGJIWO",
#     "213": "KEPUTRAN UTARA",
#     "214": "KEPUTRAN SELATAN",
#     "215": "DINOYO TANGSI",
#     "216": "KAYOON",
#     "217": "KRUKAH",
#     "218": "PACAR KELING",
#     "219": "INDRAKILA INDUK",
#     "220": "INDRAKILA DRT",
#     "221": "AMBENGAN BATU",
#     "222": "JL. KELAPA",
#     "223": "SUTOREJO",
#     "224": "KALI KEDINDING",
#     "225": "PUCANG ANOM",
#     "226": "RUNGKUT BARU",
#     "227": "TAMBAH REJO",
#     "228": "KAPASAN BARU",
#     "301": "ASEM ROWO",
#     "302": "TIDAR",
#     "303": "TEMBOK DUKUH",
#     "304": "BABA'AN",
#     "305": "KEBALEN BARAT DRT",
#     "306": "BALONGSARI",
#     "307": "MANUKAN KULON",
#     "308": "BANJAR SUGIHAN",
#     "309": "BLAURAN BARU",
#     "310": "KOBLEN",
#     "311": "KEPATIHAN",
#     "312": "DUPAK BANDEROJO",
#     "313": "DUPAK BANGUNREJO",
#     "314": "DUPAK RUKUN",
#     "315": "KREMBANGAN",
#     "316": "PESAPEN",
#     "317": "PESAPEN CIKAR",
#     "318": "JL GRESIK",
#     "319": "JEMBATAN MERAH",
#     "320": "PABEAN",
#     "321": "BIBIS",
#     "322": "JL. DUKUH",
#     "323": "PECINDILAN",
#     "324": "KALIANYAR",
#     "325": "GEMBONG TEBASAN",
#     "326": "GEMBONG TEBASAN DRT",
#     "327": "JAGALAN",
#     "328": "PEGIRIAN",
#     "329": "AMPEL",
#     "330": "SUKODONO",
#     "331": "SIMO",
#     "332": "SIMO GUNUNG",
#     "333": "SIMO MULYO",
#     "334": "WONOKUSUMO",
# }

# ALIASES = {
#     "tgl bayar": "tgl_bayar",
#     "tanggal bayar": "tgl_bayar",
#     "tgl pembayaran": "tgl_bayar",
#     "tanggal pembayaran": "tgl_bayar",
#     "tgl closing": "tgl_closing",
#     "tanggal closing": "tgl_closing",
#     "pasar": "pasar",
#     "nama pasar": "nama_pasar",
#     "alamat": "alamat",
#     "stand": "stand",
#     "pedagang": "pedagang",
#     "nama pedagang": "pedagang",
#     "periode": "periode",
#     "nilai": "nilai",
#     "nilai tagihan": "nilai",
#     "nominal": "nilai",
#     "kode cabang": "kode_cabang",
#     "cabang": "cabang",
#     "jenis tagihan": "jenis_tagihan",
#     "jenis": "jenis_tagihan",
# }


# # =========================================================
# # HELPER: BERSIHKAN KARAKTER ANEH (sama seperti Streamlit)
# # =========================================================
# def _bersihkan_text(value):
#     """
#     Bersihkan karakter aneh dari nilai teks:
#     - \r, \n, \t → spasi
#     - _x000D_, _x000A_, _x0009_ (artefak Excel) → spasi
#     - Strip spasi depan/belakang
#     """
#     if pd.isna(value) or value is None:
#         return ""
#     s = str(value)
#     s = s.replace("\r", " ").replace("\n", " ").replace("\t", " ")
#     s = s.replace("_x000D_", " ").replace("_x000A_", " ").replace("_x0009_", " ")
#     s = s.strip()
#     if s.lower() in ("nan", "none", "null"):
#         return ""
#     return s


# def normalize_header(value):
#     text = str(value).strip().lower()
#     text = re.sub(r"[_\-]+", " ", text)
#     text = re.sub(r"\s+", " ", text)
#     return text


# def parse_filename(filename):
#     stem = filename.rsplit("/", 1)[-1]
#     stem = re.sub(r"\.(xlsx|xls)$", "", stem, flags=re.I).strip()
#     match = re.match(r"^(\d+)\s+([ALT])(?:\s+(.*))?$", stem, flags=re.I)
#     if not match:
#         raise ValueError(
#             f"Nama file '{filename}' tidak sesuai. Gunakan contoh: "
#             "'100 A 2020-2025.xlsx'."
#         )

#     kode = match.group(1)
#     jenis_kode = match.group(2).upper()
#     periode = (match.group(3) or "").strip()
#     return {
#         "kode_cabang": kode,
#         "cabang": KODE_CABANG.get(kode, kode),
#         "jenis_tagihan": KODE_JENIS.get(jenis_kode, jenis_kode),
#         "periode_filename": periode,
#     }


# def _clean_text(value):
#     """Wrapper ke _bersihkan_text — biar kompatibel dengan kode lama."""
#     return _bersihkan_text(value)


# def _clean_decimal(value):
#     if pd.isna(value) or value == "":
#         return Decimal("0")
#     if isinstance(value, (int, float)):
#         return Decimal(str(value))
#     text = str(value).strip().replace("Rp", "").replace("rp", "").replace(" ", "")
#     # Handle Indonesian formats such as 1.234.567,89 and plain 1234567.89.
#     if "," in text and "." in text:
#         if text.rfind(",") > text.rfind("."):
#             text = text.replace(".", "").replace(",", ".")
#         else:
#             text = text.replace(",", "")
#     elif "," in text:
#         text = text.replace(".", "").replace(",", ".")
#     else:
#         # Indonesian currency commonly uses dots as thousands separators:
#         # 125.000 -> 125000, while 125.50 is kept as a decimal.
#         parts = text.split(".")
#         if len(parts) > 1:
#             if all(part.isdigit() for part in parts) and len(parts[-1]) == 3:
#                 text = "".join(parts)
#             elif len(parts) > 2:
#                 text = "".join(parts)
#     try:
#         return Decimal(text or "0")
#     except (InvalidOperation, ValueError):
#         return Decimal("0")


# def _to_date(value):
#     if pd.isna(value) or value == "":
#         return None
#     parsed = pd.to_datetime(value, errors="coerce", dayfirst=True)
#     if pd.isna(parsed):
#         return None
#     return parsed.date()


# def _derive_year_month(row, filename_info):
#     for key in ("tgl_bayar", "tgl_closing"):
#         date_value = row.get(key)
#         if date_value:
#             return date_value.year, date_value.month

#     years = re.findall(r"(?:19|20)\d{2}", filename_info.get("periode_filename", ""))
#     if years:
#         return int(years[0]), None

#     period = _clean_text(row.get("periode", ""))
#     years = re.findall(r"(?:19|20)\d{2}", period)
#     if years:
#         return int(years[0]), None

#     return None, None


# # =========================================================
# # READ EXCEL FILE
# # =========================================================
# def read_excel_file(file_obj):
#     info = parse_filename(file_obj.name)
#     try:
#         workbook = pd.read_excel(file_obj, sheet_name=0)
#     except Exception as exc:
#         raise ValueError(f"Gagal membaca '{file_obj.name}': {exc}") from exc

#     if workbook.empty:
#         raise ValueError(f"'{file_obj.name}' tidak memiliki data.")

#     renamed = {}
#     for column in workbook.columns:
#         key = normalize_header(column)
#         if key in ALIASES:
#             renamed[column] = ALIASES[key]
#     workbook = workbook.rename(columns=renamed)

#     # Some files use the code/metadata only in the filename. Missing columns
#     # are therefore allowed and filled safely.
#     for column in ALIASES.values():
#         if column not in workbook.columns:
#             workbook[column] = ""

#     rows = []
#     for _, raw in workbook.iterrows():
#         row = {column: raw.get(column, "") for column in ALIASES.values()}
#         tgl_bayar = _to_date(row["tgl_bayar"])
#         tgl_closing = _to_date(row["tgl_closing"])
#         row["tgl_bayar"] = tgl_bayar
#         row["tgl_closing"] = tgl_closing

#         row["kode_cabang"] = _clean_text(row["kode_cabang"]) or info["kode_cabang"]
#         row["cabang"] = _clean_text(row["cabang"]) or info["cabang"]
#         row["jenis_tagihan"] = _clean_text(row["jenis_tagihan"]) or info["jenis_tagihan"]

#         # ⭐ BERSIHKAN SEMUA KOLOM TEKS
#         row["pasar"] = _clean_text(row["pasar"])
#         row["nama_pasar"] = _clean_text(row["nama_pasar"]) or row["pasar"]
#         row["alamat"] = _clean_text(row["alamat"])
#         row["stand"] = _clean_text(row["stand"])
#         row["pedagang"] = _clean_text(row["pedagang"])
#         row["periode"] = _clean_text(row["periode"]) or info["periode_filename"]
#         row["nilai"] = _clean_decimal(row["nilai"])
#         row["sumber_file"] = file_obj.name

#         # ⭐ MAPPING NAMA PASAR (kode → nama, sama seperti Streamlit)
#         if row["pasar"] in KODE_PASAR:
#             row["nama_pasar"] = KODE_PASAR[row["pasar"]]
#         elif not row["nama_pasar"]:
#             row["nama_pasar"] = "TIDAK DIKETAHUI"

#         year, month = _derive_year_month(row, info)
#         row["tahun"] = year
#         row["bulan"] = month
#         row["tahun_bulan"] = f"{year:04d}-{month:02d}" if year and month else (
#             f"{year:04d}" if year else ""
#         )

#         # ⭐ FILTER TAHUN DINAMIS (sama seperti Streamlit)
#         if year is None:
#             # Skip baris tanpa tahun (tidak bisa difilter)
#             continue
#         if not (TAHUN_MINIMAL <= year <= TAHUN_MAKSIMAL):
#             # Skip tahun di luar range
#             continue

#         # Skip completely blank records.
#         meaningful = any([
#             row["nama_pasar"], row["stand"], row["pedagang"],
#             row["periode"], row["nilai"] != 0,
#         ])
#         if meaningful:
#             rows.append(row)

#     return rows


# # =========================================================
# # PREPROCESS FILES
# # =========================================================
# def preprocess_files(files):
#     rows = []
#     errors = []
#     successful_files = []

#     for file_obj in files:
#         try:
#             file_rows = read_excel_file(file_obj)
#             if not file_rows:
#                 raise ValueError("Tidak ada baris data yang dapat diproses.")
#             rows.extend(file_rows)
#             successful_files.append(file_obj.name)
#         except Exception as exc:
#             errors.append(str(exc))

#     return rows, errors, successful_files


# # =========================================================
# # SIMPAN KE DATABASE
# # =========================================================
# def save_rows(rows, replace_all=False):
#     if not rows:
#         return 0

#     if replace_all:
#         TagihanPasar.objects.all().delete()

#     existing = set(
#         TagihanPasar.objects.values_list("sumber_file", flat=True).distinct()
#     )
#     seen_files = set()
#     new_rows = []
#     for row in rows:
#         source = row["sumber_file"]
#         if source in existing or source in seen_files:
#             continue
#         seen_files.add(source)
#         new_rows.append(row)

#     if not new_rows:
#         return 0

#     objects = [TagihanPasar(**row) for row in new_rows]
#     TagihanPasar.objects.bulk_create(objects, batch_size=1000)
#     return len(objects)


# def get_existing_files():
#     return list(
#         TagihanPasar.objects.values_list("sumber_file", flat=True)
#         .distinct()
#         .order_by("sumber_file")
#     )

# import os
# import re
# from datetime import datetime
# from decimal import Decimal, InvalidOperation

# import pandas as pd

# from dashboard.models import TagihanPasar


# # =========================================================
# # KONFIGURASI TAHUN
# # =========================================================
# TAHUN_MINIMAL = 2010
# TAHUN_MAKSIMAL = datetime.now().year + 1


# # =========================================================
# # MAPPING
# # =========================================================
# MAPPING_CABANG = {
#     "100": "Selatan",
#     "200": "Timur",
#     "300": "Utara"
# }

# MAPPING_JENIS = {
#     "A": "Air",
#     "T": "Tempat",
#     "L": "Listrik"
# }

# MAPPING_PASAR = {
#     "101": "BENDUL MERISI",
#     "102": "GAYUNG SARI",
#     "103": "WONOKROMO LAMA",
#     "104": "DUKUH KUPANG",
#     "105": "DUKUH KUPANG BARAT",
#     "106": "GENTENG BARU",
#     "107": "KARANG PILANG",
#     "108": "LAKARSANTRI",
#     "109": "BANGKINGAN",
#     "110": "HWN KARANG PILANG",
#     "111": "KEMBANG",
#     "112": "KEDUNGSARI",
#     "113": "KEDUNGDORO",
#     "114": "KUPANG",
#     "115": "PANDEGILING",
#     "116": "KUPANG GUNUNG",
#     "117": "PAKIS",
#     "118": "WONOKITRI",
#     "119": "TUNJUNGAN",
#     "120": "WONOKROMO",
#     "201": "BUNGA BRATANG",
#     "202": "BURUNG BRATANG",
#     "203": "INPRES BRATANG",
#     "204": "KEPUTIH",
#     "205": "GUBENG MASJID",
#     "206": "GUBENG KERTAJAYA",
#     "207": "KAPASAN",
#     "208": "ASWOTOMO",
#     "209": "KERTOPATEN",
#     "210": "KENDANGSARI",
#     "211": "TENGGILIS",
#     "212": "PANJANGJIWO",
#     "213": "KEPUTRAN UTARA",
#     "214": "KEPUTRAN SELATAN",
#     "215": "DINOYO TANGSI",
#     "216": "KAYOON",
#     "217": "KRUKAH",
#     "218": "PACAR KELING",
#     "219": "INDRAKILA INDUK",
#     "220": "INDRAKILA DRT",
#     "221": "AMBENGAN BATU",
#     "222": "JL. KELAPA",
#     "223": "SUTOREJO",
#     "224": "KALI KEDINDING",
#     "225": "PUCANG ANOM",
#     "226": "RUNGKUT BARU",
#     "227": "TAMBAH REJO",
#     "228": "KAPASAN BARU",
#     "301": "ASEM ROWO",
#     "302": "TIDAR",
#     "303": "TEMBOK DUKUH",
#     "304": "BABA'AN",
#     "305": "KEBALEN BARAT DRT",
#     "306": "BALONGSARI",
#     "307": "MANUKAN KULON",
#     "308": "BANJAR SUGIHAN",
#     "309": "BLAURAN BARU",
#     "310": "KOBLEN",
#     "311": "KEPATIHAN",
#     "312": "DUPAK BANDEROJO",
#     "313": "DUPAK BANGUNREJO",
#     "314": "DUPAK RUKUN",
#     "315": "KREMBANGAN",
#     "316": "PESAPEN",
#     "317": "PESAPEN CIKAR",
#     "318": "JL GRESIK",
#     "319": "JEMBATAN MERAH",
#     "320": "PABEAN",
#     "321": "BIBIS",
#     "322": "JL. DUKUH",
#     "323": "PECINDILAN",
#     "324": "KALIANYAR",
#     "325": "GEMBONG TEBASAN",
#     "326": "GEMBONG TEBASAN DRT",
#     "327": "JAGALAN",
#     "328": "PEGIRIAN",
#     "329": "AMPEL",
#     "330": "SUKODONO",
#     "331": "SIMO",
#     "332": "SIMO GUNUNG",
#     "333": "SIMO MULYO",
#     "334": "WONOKUSUMO"
# }

# KOLOM_DIBUTUHAN = [
#     "tglbayar", "tglclosing", "pasar", "alamat",
#     "stand", "pedagang", "periode", "nilai"
# ]


# # =========================================================
# # HELPER: BERSIHKAN KARAKTER ANEH
# # =========================================================
# def _bersihkan_text(x):
#     """
#     Bersihkan karakter aneh dari nilai teks:
#     - \\r, \\n, \\t → spasi
#     - _x000D_, _x000A_, _x0009_ (artefak Excel) → spasi
#     - Strip spasi depan/belakang
#     """
#     if x is None or pd.isna(x):
#         return ""
#     s = str(x)
#     s = s.replace("\r", " ").replace("\n", " ").replace("\t", " ")
#     s = s.replace("_x000D_", " ").replace("_x000A_", " ").replace("_x0009_", " ")
#     s = s.strip()
#     if s == "" or s.lower() in ("nan", "none", "null"):
#         return ""
#     return s


# # =========================================================
# # PARSE FILENAME
# # =========================================================
# def parse_filename(filename):
#     """
#     Parse nama file dengan pola: '<kode_cabang> <kode_jenis> <sisa>'
#     Contoh: '100 A januari 2020.xlsx' → kode=100, jenis=A, periode='januari 2020'
#     """
#     # Ambil nama file saja (buang path kalau ada)
#     stem = filename.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
#     # Buang ekstensi
#     stem = re.sub(r"\.(xlsx|xls)$", "", stem, flags=re.I).strip()

#     bagian = stem.split()

#     if len(bagian) < 2:
#         raise ValueError(
#             f"Nama file '{filename}' tidak sesuai. Gunakan contoh: "
#             "'100 A januari 2020.xlsx'."
#         )

#     kode_cabang = bagian[0]
#     kode_jenis = bagian[1].upper()
#     periode = " ".join(bagian[2:]).strip() if len(bagian) > 2 else ""

#     if kode_cabang not in MAPPING_CABANG:
#         raise ValueError(
#             f"Nama file '{filename}': kode cabang '{kode_cabang}' tidak dikenal. "
#             f"Gunakan 100, 200, atau 300."
#         )

#     if kode_jenis not in MAPPING_JENIS:
#         raise ValueError(
#             f"Nama file '{filename}': kode jenis '{kode_jenis}' tidak dikenal. "
#             f"Gunakan A, T, atau L."
#         )

#     return {
#         "kode_cabang": kode_cabang,
#         "cabang": MAPPING_CABANG[kode_cabang],
#         "jenis_tagihan": MAPPING_JENIS[kode_jenis],
#         "periode_filename": periode,
#     }


# # =========================================================
# # BACA EXCEL FILE (sama seperti Streamlit)
# # =========================================================
# def read_excel_file(file_obj):
#     """
#     Baca satu file Excel, return list of dict siap simpan ke model TagihanPasar.
#     """
#     info = parse_filename(file_obj.name)

#     try:
#         df = pd.read_excel(
#             file_obj,
#             dtype={"pasar": "string", "stand": "string"}
#         )
#     except Exception as exc:
#         raise ValueError(f"Gagal membaca '{file_obj.name}': {exc}") from exc

#     if df.empty:
#         raise ValueError(f"'{file_obj.name}' tidak memiliki data.")

#     # Cek kolom wajib
#     kolom_hilang = [k for k in KOLOM_DIBUTUHAN if k not in df.columns]
#     if kolom_hilang:
#         raise ValueError(
#             f"'{file_obj.name}': kolom hilang {kolom_hilang}. "
#             f"Kolom yang dibutuhkan: {KOLOM_DIBUTUHAN}"
#         )

#     # Ambil hanya kolom yang dibutuhkan
#     df = df[KOLOM_DIBUTUHAN].copy()

#     # Metadata dari nama file
#     df["Kode Cabang"] = info["kode_cabang"]
#     df["Cabang"] = info["cabang"]
#     df["Jenis Tagihan"] = info["jenis_tagihan"]
#     df["Sumber File"] = file_obj.name

#     # Rename ke nama kolom internal
#     df = df.rename(columns={
#         "tglbayar": "tgl_bayar",
#         "tglclosing": "tgl_closing",
#         "pasar": "pasar",
#         "alamat": "alamat",
#         "stand": "stand",
#         "pedagang": "pedagang",
#         "periode": "periode",
#         "nilai": "nilai",
#     })

#     # ===== KONVERSI TANGGAL (format eksplisit seperti Streamlit) =====
#     df["tgl_bayar"] = pd.to_datetime(
#         df["tgl_bayar"], format="%d/%m/%Y %H:%M:%S", errors="coerce"
#     )
#     df["tgl_closing"] = pd.to_datetime(
#         df["tgl_closing"], format="%d/%m/%Y %H:%M:%S", errors="coerce"
#     )

#     # Kolom turunan tahun/bulan
#     df["tahun"] = df["tgl_bayar"].dt.year
#     df["bulan"] = df["tgl_bayar"].dt.month
#     df["tahun_bulan"] = df["tgl_bayar"].dt.to_period("M").astype(str)

#     # ===== BERSIHKAN KOLOM TEKS =====
#     for col in ["pasar", "alamat", "stand", "pedagang", "periode"]:
#         df[col] = df[col].apply(_bersihkan_text)

#     # ===== KONVERSI NILAI NUMERIK =====
#     df["nilai"] = pd.to_numeric(df["nilai"], errors="coerce").fillna(0)

#     # ===== MAPPING NAMA PASAR =====
#     df["nama_pasar"] = df["pasar"].map(MAPPING_PASAR).fillna("TIDAK DIKETAHUI")

#     # ===== FILTER TAHUN DINAMIS =====
#     df = df[
#         df["tahun"].between(TAHUN_MINIMAL, TAHUN_MAKSIMAL, inclusive="both")
#     ].reset_index(drop=True)

#     # ===== KONVERSI KE LIST OF DICT untuk bulk_create =====
#     rows = []
#     for _, r in df.iterrows():
#         # Skip kalau tahun kosong (tanggal tidak valid)
#         if pd.isna(r["tahun"]):
#             continue

#         # Skip baris yang isinya kosong semua
#         meaningful = any([
#             _bersihkan_text(r["nama_pasar"]),
#             _bersihkan_text(r["stand"]),
#             _bersihkan_text(r["pedagang"]),
#             _bersihkan_text(r["periode"]),
#             r["nilai"] != 0,
#         ])
#         if not meaningful:
#             continue

#         # Konversi tanggal ke date object
#         tgl_bayar = r["tgl_bayar"].date() if pd.notna(r["tgl_bayar"]) else None
#         tgl_closing = r["tgl_closing"].date() if pd.notna(r["tgl_closing"]) else None

#         rows.append({
#             "tgl_bayar": tgl_bayar,
#             "tgl_closing": tgl_closing,
#             "pasar": _bersihkan_text(r["pasar"]),
#             "nama_pasar": _bersihkan_text(r["nama_pasar"]),
#             "alamat": _bersihkan_text(r["alamat"]),
#             "stand": _bersihkan_text(r["stand"]),
#             "pedagang": _bersihkan_text(r["pedagang"]),
#             "periode": _bersihkan_text(r["periode"]),
#             "nilai": Decimal(str(r["nilai"])) if pd.notna(r["nilai"]) else Decimal("0"),
#             "kode_cabang": str(r["Kode Cabang"]),
#             "cabang": _bersihkan_text(r["Cabang"]),
#             "jenis_tagihan": _bersihkan_text(r["Jenis Tagihan"]),
#             "sumber_file": file_obj.name,
#             "tahun": int(r["tahun"]) if pd.notna(r["tahun"]) else None,
#             "bulan": int(r["bulan"]) if pd.notna(r["bulan"]) else None,
#             "tahun_bulan": _bersihkan_text(r["tahun_bulan"]),
#         })

#     return rows


# # =========================================================
# # PREPROCESS FILES (untuk banyak file)
# # =========================================================
# def preprocess_files(files):
#     """
#     Preprocess banyak file sekaligus.
#     Return: (rows, errors, successful_files)
#     """
#     rows = []
#     errors = []
#     successful_files = []

#     for file_obj in files:
#         try:
#             file_rows = read_excel_file(file_obj)
#             if not file_rows:
#                 raise ValueError("Tidak ada baris data yang dapat diproses.")
#             rows.extend(file_rows)
#             successful_files.append(file_obj.name)
#         except Exception as exc:
#             errors.append(str(exc))

#     return rows, errors, successful_files


# # =========================================================
# # SIMPAN KE DATABASE LOKAL DJANGO
# # =========================================================
# def save_rows(rows, replace_all=False):
#     """
#     Simpan list of dict ke database.
#     - replace_all=False (default): append. File yang sudah ada di-skip.
#     - replace_all=True: hapus semua, ganti baru.
#     Return: jumlah baris yang di-insert.
#     """
#     if not rows:
#         return 0

#     if replace_all:
#         TagihanPasar.objects.all().delete()

#     existing = set(
#         TagihanPasar.objects.values_list("sumber_file", flat=True).distinct()
#     )
#     seen_files = set()
#     new_rows = []
#     for row in rows:
#         source = row["sumber_file"]
#         if source in existing or source in seen_files:
#             continue
#         seen_files.add(source)
#         new_rows.append(row)

#     if not new_rows:
#         return 0

#     objects = [TagihanPasar(**row) for row in new_rows]
#     TagihanPasar.objects.bulk_create(objects, batch_size=1000)
#     return len(objects)


# # =========================================================
# # GET EXISTING FILES
# # =========================================================
# def get_existing_files():
#     return list(
#         TagihanPasar.objects.values_list("sumber_file", flat=True)
#         .distinct()
#         .order_by("sumber_file")
#     )

import os
import re
from datetime import datetime
from decimal import Decimal, InvalidOperation

import pandas as pd

from dashboard.models import TagihanPasar


# =========================================================
# KONFIGURASI TAHUN
# =========================================================
TAHUN_MINIMAL = 2010
TAHUN_MAKSIMAL = datetime.now().year + 1


# =========================================================
# MAPPING
# =========================================================
MAPPING_CABANG = {
    "100": "Selatan",
    "200": "Timur",
    "300": "Utara"
}

MAPPING_JENIS = {
    "A": "Air",
    "T": "Tempat",
    "L": "Listrik"
}

MAPPING_PASAR = {
    "101": "BENDUL MERISI",
    "102": "GAYUNG SARI",
    "103": "WONOKROMO LAMA",
    "104": "DUKUH KUPANG",
    "105": "DUKUH KUPANG BARAT",
    "106": "GENTENG BARU",
    "107": "KARANG PILANG",
    "108": "LAKARSANTRI",
    "109": "BANGKINGAN",
    "110": "HWN KARANG PILANG",
    "111": "KEMBANG",
    "112": "KEDUNGSARI",
    "113": "KEDUNGDORO",
    "114": "KUPANG",
    "115": "PANDEGILING",
    "116": "KUPANG GUNUNG",
    "117": "PAKIS",
    "118": "WONOKITRI",
    "119": "TUNJUNGAN",
    "120": "WONOKROMO",
    "201": "BUNGA BRATANG",
    "202": "BURUNG BRATANG",
    "203": "INPRES BRATANG",
    "204": "KEPUTIH",
    "205": "GUBENG MASJID",
    "206": "GUBENG KERTAJAYA",
    "207": "KAPASAN",
    "208": "ASWOTOMO",
    "209": "KERTOPATEN",
    "210": "KENDANGSARI",
    "211": "TENGGILIS",
    "212": "PANJANGJIWO",
    "213": "KEPUTRAN UTARA",
    "214": "KEPUTRAN SELATAN",
    "215": "DINOYO TANGSI",
    "216": "KAYOON",
    "217": "KRUKAH",
    "218": "PACAR KELING",
    "219": "INDRAKILA INDUK",
    "220": "INDRAKILA DRT",
    "221": "AMBENGAN BATU",
    "222": "JL. KELAPA",
    "223": "SUTOREJO",
    "224": "KALI KEDINDING",
    "225": "PUCANG ANOM",
    "226": "RUNGKUT BARU",
    "227": "TAMBAH REJO",
    "228": "KAPASAN BARU",
    "301": "ASEM ROWO",
    "302": "TIDAR",
    "303": "TEMBOK DUKUH",
    "304": "BABA'AN",
    "305": "KEBALEN BARAT DRT",
    "306": "BALONGSARI",
    "307": "MANUKAN KULON",
    "308": "BANJAR SUGIHAN",
    "309": "BLAURAN BARU",
    "310": "KOBLEN",
    "311": "KEPATIHAN",
    "312": "DUPAK BANDEROJO",
    "313": "DUPAK BANGUNREJO",
    "314": "DUPAK RUKUN",
    "315": "KREMBANGAN",
    "316": "PESAPEN",
    "317": "PESAPEN CIKAR",
    "318": "JL GRESIK",
    "319": "JEMBATAN MERAH",
    "320": "PABEAN",
    "321": "BIBIS",
    "322": "JL. DUKUH",
    "323": "PECINDILAN",
    "324": "KALIANYAR",
    "325": "GEMBONG TEBASAN",
    "326": "GEMBONG TEBASAN DRT",
    "327": "JAGALAN",
    "328": "PEGIRIAN",
    "329": "AMPEL",
    "330": "SUKODONO",
    "331": "SIMO",
    "332": "SIMO GUNUNG",
    "333": "SIMO MULYO",
    "334": "WONOKUSUMO"
}

KOLOM_DIBUTUHAN = [
    "tglbayar", "tglclosing", "pasar", "alamat",
    "stand", "pedagang", "periode", "nilai"
]


# =========================================================
# HELPER: BERSIHKAN KARAKTER ANEH
# =========================================================
def _bersihkan_text(x):
    """
    Bersihkan karakter aneh dari nilai teks:
    - \r, \n, \t → spasi
    - _x000D_, _x000A_, _x0009_ (artefak Excel) → spasi
    - Strip spasi depan/belakang
    """
    if x is None or pd.isna(x):
        return ""
    s = str(x)
    s = s.replace("\r", " ").replace("\n", " ").replace("\t", " ")
    s = s.replace("_x000D_", " ").replace("_x000A_", " ").replace("_x0009_", " ")
    s = s.strip()
    if s == "" or s.lower() in ("nan", "none", "null"):
        return ""
    return s


# =========================================================
# PARSE FILENAME
# =========================================================
def parse_filename(filename):
    """
    Parse nama file dengan pola: '<kode_cabang> <kode_jenis> <sisa>'
    Contoh: '100 A januari 2020.xlsx' → kode=100, jenis=A, periode='januari 2020'
    """
    stem = filename.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
    stem = re.sub(r"\.(xlsx|xls)$", "", stem, flags=re.I).strip()

    bagian = stem.split()

    if len(bagian) < 2:
        raise ValueError(
            f"Nama file '{filename}' tidak sesuai. Gunakan contoh: "
            "'100 A januari 2020.xlsx'."
        )

    kode_cabang = bagian[0]
    kode_jenis = bagian[1].upper()
    periode = " ".join(bagian[2:]).strip() if len(bagian) > 2 else ""

    if kode_cabang not in MAPPING_CABANG:
        raise ValueError(
            f"Nama file '{filename}': kode cabang '{kode_cabang}' tidak dikenal. "
            f"Gunakan 100, 200, atau 300."
        )

    if kode_jenis not in MAPPING_JENIS:
        raise ValueError(
            f"Nama file '{filename}': kode jenis '{kode_jenis}' tidak dikenal. "
            f"Gunakan A, T, atau L."
        )

    return {
        "kode_cabang": kode_cabang,
        "cabang": MAPPING_CABANG[kode_cabang],
        "jenis_tagihan": MAPPING_JENIS[kode_jenis],
        "periode_filename": periode,
    }


# =========================================================
# BACA EXCEL FILE
# =========================================================
def read_excel_file(file_obj):
    """
    Baca satu file Excel, return list of dict siap simpan ke model TagihanPasar.
    """
    info = parse_filename(file_obj.name)

    try:
        df = pd.read_excel(
            file_obj,
            dtype={"pasar": "string", "stand": "string"}
        )
    except Exception as exc:
        raise ValueError(f"Gagal membaca '{file_obj.name}': {exc}") from exc

    if df.empty:
        raise ValueError(f"'{file_obj.name}' tidak memiliki data.")

    # Cek kolom wajib
    kolom_hilang = [k for k in KOLOM_DIBUTUHAN if k not in df.columns]
    if kolom_hilang:
        raise ValueError(
            f"'{file_obj.name}': kolom hilang {kolom_hilang}. "
            f"Kolom yang dibutuhkan: {KOLOM_DIBUTUHAN}"
        )

    # Ambil hanya kolom yang dibutuhkan
    df = df[KOLOM_DIBUTUHAN].copy()

    # Metadata dari nama file
    df["Kode Cabang"] = info["kode_cabang"]
    df["Cabang"] = info["cabang"]
    df["Jenis Tagihan"] = info["jenis_tagihan"]
    df["Sumber File"] = file_obj.name

    # Rename ke nama kolom internal
    df = df.rename(columns={
        "tglbayar": "tgl_bayar",
        "tglclosing": "tgl_closing",
        "pasar": "pasar",
        "alamat": "alamat",
        "stand": "stand",
        "pedagang": "pedagang",
        "periode": "periode",
        "nilai": "nilai",
    })

    # ===== KONVERSI TANGGAL =====
    df["tgl_bayar"] = pd.to_datetime(
        df["tgl_bayar"], format="%d/%m/%Y %H:%M:%S", errors="coerce"
    )
    df["tgl_closing"] = pd.to_datetime(
        df["tgl_closing"], format="%d/%m/%Y %H:%M:%S", errors="coerce"
    )

    # Kolom turunan tahun/bulan
    df["tahun"] = df["tgl_bayar"].dt.year
    df["bulan"] = df["tgl_bayar"].dt.month
    df["tahun_bulan"] = df["tgl_bayar"].dt.to_period("M").astype(str)

    # ===== BERSIHKAN KOLOM TEKS =====
    for col in ["pasar", "alamat", "stand", "pedagang", "periode"]:
        df[col] = df[col].apply(_bersihkan_text)

    # ===== KONVERSI NILAI NUMERIK =====
    df["nilai"] = pd.to_numeric(df["nilai"], errors="coerce").fillna(0)

    # ===== MAPPING NAMA PASAR =====
    df["nama_pasar"] = df["pasar"].map(MAPPING_PASAR).fillna("TIDAK DIKETAHUI")

    # ===== FILTER TAHUN DINAMIS =====
    df = df[
        df["tahun"].between(TAHUN_MINIMAL, TAHUN_MAKSIMAL, inclusive="both")
    ].reset_index(drop=True)

    # ===== KONVERSI KE LIST OF DICT untuk bulk_create =====
    rows = []
    for _, r in df.iterrows():
        # Skip kalau tahun kosong (tanggal tidak valid)
        if pd.isna(r["tahun"]):
            continue

        # Skip baris yang isinya kosong semua
        meaningful = any([
            _bersihkan_text(r["nama_pasar"]),
            _bersihkan_text(r["stand"]),
            _bersihkan_text(r["pedagang"]),
            _bersihkan_text(r["periode"]),
            r["nilai"] != 0,
        ])
        if not meaningful:
            continue

        # Konversi tanggal ke date object
        tgl_bayar = r["tgl_bayar"].date() if pd.notna(r["tgl_bayar"]) else None
        tgl_closing = r["tgl_closing"].date() if pd.notna(r["tgl_closing"]) else None

        rows.append({
            "tgl_bayar": tgl_bayar,
            "tgl_closing": tgl_closing,
            "pasar": _bersihkan_text(r["pasar"]),
            "nama_pasar": _bersihkan_text(r["nama_pasar"]),
            "alamat": _bersihkan_text(r["alamat"]),
            "stand": _bersihkan_text(r["stand"]),
            "pedagang": _bersihkan_text(r["pedagang"]),
            "periode": _bersihkan_text(r["periode"]),
            "nilai": Decimal(str(r["nilai"])) if pd.notna(r["nilai"]) else Decimal("0"),
            "kode_cabang": str(r["Kode Cabang"]),
            "cabang": _bersihkan_text(r["Cabang"]),
            "jenis_tagihan": _bersihkan_text(r["Jenis Tagihan"]),
            "sumber_file": file_obj.name,
            "tahun": int(r["tahun"]) if pd.notna(r["tahun"]) else None,
            "bulan": int(r["bulan"]) if pd.notna(r["bulan"]) else None,
            "tahun_bulan": _bersihkan_text(r["tahun_bulan"]),
        })

    return rows


# =========================================================
# PREPROCESS FILES
# =========================================================
def preprocess_files(files):
    """
    Preprocess banyak file sekaligus.
    Return: (rows, errors, successful_files)
    """
    rows = []
    errors = []
    successful_files = []

    for file_obj in files:
        try:
            file_rows = read_excel_file(file_obj)
            if not file_rows:
                raise ValueError("Tidak ada baris data yang dapat diproses.")
            rows.extend(file_rows)
            successful_files.append(file_obj.name)
        except Exception as exc:
            errors.append(str(exc))

    return rows, errors, successful_files


# =========================================================
# SIMPAN KE DATABASE — ⭐ FIXED: TIDAK SKIP BARIS DARI FILE SAMA
# =========================================================
def save_rows(rows, replace_all=False):
    """
    Simpan list of dict ke database.

    Mode:
        - replace_all=False (default): APPEND.
          File yang SUDAH ADA di database (dicek dari 'sumber_file')
          akan di-skip SEMUA barisnya.
          File BARU akan disimpan SEMUA barisnya.
        - replace_all=True: hapus semua data lama, ganti baru.

    Return: jumlah baris yang di-insert.
    """
    if not rows:
        return 0

    if replace_all:
        TagihanPasar.objects.all().delete()

    # ⭐ Ambil daftar file yang SUDAH ADA di database (SEBELUM upload ini)
    existing_files = set(
        TagihanPasar.objects.values_list("sumber_file", flat=True).distinct()
    )

    # ⭐ Filter: buang SEMUA baris dari file yang sudah ada di database
    # Baris dari file yang SAMA dalam batch ini TIDAK di-skip
    new_rows = []
    for row in rows:
        if row["sumber_file"] in existing_files:
            continue
        new_rows.append(row)

    if not new_rows:
        return 0

    # Bulk insert SEMUA baris dari file baru
    objects = [TagihanPasar(**row) for row in new_rows]
    TagihanPasar.objects.bulk_create(objects, batch_size=1000)
    return len(objects)


# =========================================================
# GET EXISTING FILES
# =========================================================
def get_existing_files():
    return list(
        TagihanPasar.objects.values_list("sumber_file", flat=True)
        .distinct()
        .order_by("sumber_file")
    )