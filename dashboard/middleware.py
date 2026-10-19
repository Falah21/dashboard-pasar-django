import os
from django.shortcuts import render


class MaintenanceModeMiddleware:
    """
    Middleware untuk mode maintenance.
    
    Aktifkan dengan env variable: MAINTENANCE_MODE=True
    Matikan dengan: MAINTENANCE_MODE=False (atau hapus variable)
    
    Semua request akan ditolak dengan halaman maintenance,
    kecuali:
    - Admin Django (/admin/) tetap bisa akses
    - Static files (/static/, /media/) tetap bisa akses
    - Request dari IP tertentu (whitelist, opsional)
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Cek apakah maintenance mode aktif
        maintenance_mode = os.getenv("MAINTENANCE_MODE", "False").strip().lower() in {
            "1", "true", "yes", "on"
        }
        
        if maintenance_mode:
            # Bypass untuk admin, static, media
            bypass_paths = (
                "/admin/",
                "/static/",
                "/media/",
                "/favicon.ico",
            )
            
            if request.path.startswith(bypass_paths):
                return self.get_response(request)
            
            # Cek whitelist IP (opsional)
            whitelist_ips = os.getenv("MAINTENANCE_WHITELIST_IPS", "").strip()
            if whitelist_ips:
                allowed_ips = [ip.strip() for ip in whitelist_ips.split(",") if ip.strip()]
                client_ip = self._get_client_ip(request)
                if client_ip in allowed_ips:
                    return self.get_response(request)
            
            # Tampilkan halaman maintenance
            return render(request, "maintenance.html", status=503)
        
        return self.get_response(request)
    
    def _get_client_ip(self, request):
        """Ambil IP client dari header X-Forwarded-For (Railway pakai proxy)."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "")