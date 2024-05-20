from django.shortcuts import render, redirect
from django.contrib import messages
from utils.auth import verify_id_token, revoke_token


def home(request):
    if 'uid' not in request.session:
        # Jika tidak ada sesi UID, redirect pengguna ke halaman login
        return redirect('authentication:login')

    # Dapatkan token dari sesi
    token = request.session['uid']

    # Verifikasi token menggunakan fungsi utilitas
    decoded_token = verify_id_token(token)

    if not decoded_token:
        # Jika token tidak valid, redirect pengguna ke halaman login
        return redirect('authentication:login')

    # Token valid, lanjutkan untuk menampilkan halaman home
    return render(request, "Home.html")
