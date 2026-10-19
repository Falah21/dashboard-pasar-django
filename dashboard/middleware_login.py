from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect


class LoginRequiredMiddleware:
    """
    Middleware yang mewajibkan login via PIN sebelum akses halaman apapun.
    
    Pengecualian (bypass):
    - /login/           → halaman login
    - /logout/          → logout
    - /admin/           → admin Django
    - /static/          → static files
    - /media/           → media files
    - /favicon.ico      → favicon
    - /maintenance/     → maintenance (kalau ada)
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Daftar path yang TIDAK perlu login
        exempt_paths = (
            "/login/",
            "/logout/",
            "/admin/",
            "/static/",
            "/media/",
            "/favicon.ico",
        )
        
        path = request.path
        
        # Bypass path yang di-exempt
        if any(path.startswith(p) for p in exempt_paths):
            return self.get_response(request)
        
        # Cek apakah user sudah login via session
        is_logged_in = request.session.get("is_logged_in", False)
        
        if not is_logged_in:
            # Simpan URL asal biar bisa redirect balik setelah login
            request.session["next_url"] = path
            return redirect(settings.LOGIN_URL)
        
        return self.get_response(request)