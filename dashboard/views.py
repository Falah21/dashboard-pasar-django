import json
import os
from decimal import Decimal
from django.conf import settings
from django.contrib import messages
# from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import redirect, render

from .forms import UploadForm
from .models import TagihanPasar
from .utils.preprocessing import get_existing_files, preprocess_files, save_rows

# =========================================================
# VIEW: LOGIN PIN
# =========================================================
def login_view(request):
    """Halaman login dengan PIN."""
    
    # Kalau sudah login, redirect ke dashboard
    if request.session.get("is_logged_in"):
        return redirect("dashboard:index")
    
    error = None
    
    if request.method == "POST":
        pin_input = request.POST.get("pin", "").strip()
        pin_correct = settings.LOGIN_PIN
        
        if pin_input == pin_correct:
            # Set session login
            request.session["is_logged_in"] = True
            request.session["login_time"] = str(__import__("datetime").datetime.now())
            
            # Redirect ke halaman asal atau dashboard
            next_url = request.session.pop("next_url", None) or settings.LOGIN_REDIRECT_URL
            return redirect(next_url)
        else:
            error = "PIN yang Anda masukkan salah. Silakan coba lagi."
    
    return render(request, "login.html", {
        "error": error,
    })


# =========================================================
# VIEW: LOGOUT
# =========================================================
def logout_view(request):
    """Logout — hapus session."""
    request.session.flush()  # hapus semua session data
    return redirect(settings.LOGIN_URL)

# =========================================================
# FORMATTER
# =========================================================
def format_rupiah(value):
    """Rp 1.234.567"""
    try:
        number = int(Decimal(value or 0))
    except (TypeError, ValueError, ArithmeticError):
        number = 0
    return "Rp " + f"{number:,}".replace(",", ".")


def format_angka(value):
    """1.234.567"""
    try:
        return f"{int(value):,}".replace(",", ".")
    except (TypeError, ValueError):
        return "0"


def format_miliar(value):
    """Format singkat untuk KPI: Rp 44,23 M"""
    try:
        number = float(value or 0)
    except (TypeError, ValueError, ArithmeticError):
        number = 0

    if abs(number) >= 1_000_000_000:
        return f"Rp {number / 1_000_000_000:.2f} M".replace(".", ",")
    elif abs(number) >= 1_000_000:
        return f"Rp {number / 1_000_000:.2f} Jt".replace(".", ",")
    elif abs(number) >= 1_000:
        return f"Rp {number / 1_000:.1f} Rb".replace(".", ",")
    else:
        return f"Rp {number:,.0f}".replace(",", ".")


def format_rupiah_singkat(value):
    return format_miliar(value)


def safe_int_list(values):
    result = []
    for value in values:
        try:
            result.append(int(value))
        except (TypeError, ValueError):
            pass
    return result


# =========================================================
# VIEW: INDEX
# =========================================================
# @login_required
def index(request):
    base_qs = TagihanPasar.objects.all()

    # ===== FILTER OPTIONS =====
    tahun_opts = list(
        base_qs.exclude(tahun__isnull=True)
        .values_list("tahun", flat=True)
        .distinct()
        .order_by("tahun")
    )
    cabang_opts = list(
        base_qs.exclude(cabang="")
        .values_list("cabang", flat=True)
        .distinct()
        .order_by("cabang")
    )
    jenis_opts = list(
        base_qs.exclude(jenis_tagihan="")
        .values_list("jenis_tagihan", flat=True)
        .distinct()
        .order_by("jenis_tagihan")
    )
    pasar_opts = list(
        base_qs.exclude(nama_pasar="")
        .values_list("nama_pasar", flat=True)
        .distinct()
        .order_by("nama_pasar")
    )

    # ===== SELECTED FILTER =====
    tahun_selected = safe_int_list(request.GET.getlist("tahun")) or [int(x) for x in tahun_opts]
    cabang_selected = request.GET.getlist("cabang") or cabang_opts
    jenis_selected = request.GET.getlist("jenis") or jenis_opts
    pasar_selected = request.GET.getlist("pasar")

    # ===== APPLY FILTER =====
    qs = base_qs
    if tahun_selected:
        qs = qs.filter(tahun__in=tahun_selected)
    if cabang_selected:
        qs = qs.filter(cabang__in=cabang_selected)
    if jenis_selected:
        qs = qs.filter(jenis_tagihan__in=jenis_selected)
    if pasar_selected:
        qs = qs.filter(nama_pasar__in=pasar_selected)

    # ===== KPI =====
    total = qs.count()
    total_nilai = qs.aggregate(total=Coalesce(Sum("nilai"), Decimal("0")))["total"]
    total_pasar = qs.exclude(nama_pasar="").values("nama_pasar").distinct().count()
    total_stand = qs.exclude(stand="").values("stand").distinct().count()
    total_pedagang = qs.exclude(pedagang="").values("pedagang").distinct().count()

    # ===== TOP PENDAPATAN PASAR =====
    top_pasar_qs = (
        qs.exclude(nama_pasar="")
        .values("nama_pasar")
        .annotate(total=Coalesce(Sum("nilai"), Decimal("0")))
        .order_by("-total")
    )
    top_pasar = []
    for idx, item in enumerate(top_pasar_qs):
        top_pasar.append({
            "rank": idx + 1,
            "nama": item["nama_pasar"],
            "nilai": float(item["total"] or 0),
            "nilai_formatted": format_rupiah_singkat(item["total"]),
        })

    # ===== CHART: NILAI TAGIHAN PER CABANG =====
    cabang_rows = list(
        qs.exclude(cabang="")
        .values("cabang")
        .annotate(total=Coalesce(Sum("nilai"), Decimal("0")))
        .order_by("-total")
    )
    chart_cabang = {
        "labels": [f"Cabang {x['cabang']}" for x in cabang_rows],
        "values": [float(x["total"] or 0) for x in cabang_rows],
    }

    # ===== CHART: DISTRIBUSI JENIS TAGIHAN =====
    urutan_jenis = ["Listrik", "Tempat", "Air"]

    jenis_rows = list(
        qs.exclude(jenis_tagihan="")
        .values("jenis_tagihan")
        .annotate(total=Coalesce(Sum("nilai"), Decimal("0")))
    )
    jenis_map = {row["jenis_tagihan"]: float(row["total"] or 0) for row in jenis_rows}

    distribusi_labels = []
    distribusi_values = []
    for jenis in urutan_jenis:
        if jenis in jenis_map:
            distribusi_labels.append(jenis)
            distribusi_values.append(jenis_map[jenis])
    for jenis, value in jenis_map.items():
        if jenis not in urutan_jenis:
            distribusi_labels.append(jenis)
            distribusi_values.append(value)

    chart_distribusi = {
        "labels": distribusi_labels,
        "values": distribusi_values,
    }

    # ===== CHART: NILAI TAGIHAN PER PASAR (Top 5) =====
    top5_names = [x["nama"] for x in top_pasar[:5]]

    market_rows = list(
        qs.filter(nama_pasar__in=top5_names)
        .values("nama_pasar", "jenis_tagihan")
        .annotate(total=Coalesce(Sum("nilai"), Decimal("0")))
    )

    market_map = {}
    for row in market_rows:
        market_map.setdefault(row["nama_pasar"], {})[row["jenis_tagihan"]] = float(row["total"] or 0)

    series = []
    for jenis in urutan_jenis:
        series.append({
            "name": jenis,
            "values": [market_map.get(name, {}).get(jenis, 0) for name in top5_names],
        })

    chart_pasar = {
        "labels": [f"Pasar {name}" for name in top5_names],
        "raw_names": top5_names,
        "series": series,
        "listrik": [market_map.get(name, {}).get("Listrik", 0) for name in top5_names],
        "tempat": [market_map.get(name, {}).get("Tempat", 0) for name in top5_names],
        "air": [market_map.get(name, {}).get("Air", 0) for name in top5_names],
    }

    # ===== CHART: TREN NILAI PER BULAN =====
    trend_rows = list(
        qs.exclude(tahun_bulan="")
        .values("tahun_bulan")
        .annotate(total=Coalesce(Sum("nilai"), Decimal("0")))
        .order_by("tahun_bulan")
    )
    chart_tren = {
        "labels": [str(x["tahun_bulan"]) for x in trend_rows],
        "values": [float(x["total"] or 0) for x in trend_rows],
    }

    # ===== TABEL DETAIL (max 500 baris) =====
    table_qs = qs.order_by("-tgl_bayar")[:500]
    table_rows = [
        {
            "tgl_bayar": item.tgl_bayar,
            "tgl_closing": item.tgl_closing,
            "cabang": item.cabang,
            "nama_pasar": item.nama_pasar,
            "alamat": item.alamat,
            "stand": item.stand,
            "pedagang": item.pedagang,
            "jenis_tagihan": item.jenis_tagihan,
            "periode": item.periode,
            "nilai_formatted": format_rupiah(item.nilai),
        }
        for item in table_qs
    ]

    # ===== CONTEXT =====
    context = {
        "no_data": not base_qs.exists(),
        "has_filtered_data": qs.exists(),
        "kpi": {
            "total_data": format_angka(total),
            "total_pendapatan": format_miliar(total_nilai),
            "total_pendapatan_full": format_rupiah(total_nilai),
            "total_pasar": format_angka(total_pasar),
            "total_stand": format_angka(total_stand),
            "total_pedagang": format_angka(total_pedagang),
        },
        "top_pasar": top_pasar,
        "chart_cabang": chart_cabang,
        "chart_pasar": chart_pasar,
        "chart_distribusi": chart_distribusi,
        "chart_tren": chart_tren,
        "table_rows": table_rows,
        "filter_opts": {
            "tahun": tahun_opts,
            "cabang": cabang_opts,
            "jenis": jenis_opts,
            "pasar": pasar_opts,
            "tahun_sel": tahun_selected,
            "cabang_sel": cabang_selected,
            "jenis_sel": jenis_selected,
            "pasar_sel": pasar_selected,
        },
    }
    return render(request, "dashboard/index.html", context)


# =========================================================
# VIEW: UPLOAD
# =========================================================
# @login_required
def upload(request):
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            files = form.cleaned_data["files"]
            replace_all = form.cleaned_data["replace_all"]
            rows, errors, successful_files = preprocess_files(files)

            if not rows:
                messages.error(request, "Tidak ada data yang berhasil diproses.")
                for error in errors:
                    messages.warning(request, error)
                return render(request, "dashboard/upload.html", {
                    "form": form,
                    "existing_files": get_existing_files(),
                })

            try:
                with transaction.atomic():
                    inserted = save_rows(rows, replace_all=replace_all)
            except Exception as exc:
                messages.error(request, f"Database gagal menyimpan data: {exc}")
                inserted = 0

            if inserted:
                messages.success(
                    request,
                    f"Berhasil menyimpan {format_angka(inserted)} baris "
                    f"dari {len(successful_files)} file."
                )
            else:
                messages.warning(
                    request,
                    "PERINGATAN!!! File ini sudah pernah diupload. File yang sudah pernah diimpor tidak akan masuk ke database."
                )

            for error in errors:
                messages.warning(request, error)

            return redirect("dashboard:upload")
    else:
        form = UploadForm()

    return render(request, "dashboard/upload.html", {
        "form": form,
        "existing_files": get_existing_files(),
    })