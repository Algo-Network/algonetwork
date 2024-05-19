from django.shortcuts import render, redirect
import pyrebase

# Konfigurasi Firebase Anda
config = {
    "apiKey": "AIzaSyCy3jcPcpSP836GBWlHVzTyb-ZInRr0o70",
    "authDomain": "algonetwork.firebaseapp.com",
    "databaseURL": "",
    "projectId": "algonetwork",
    "storageBucket": "algonetwork.appspot.com",
    "messagingSenderId": "604392656198",
    "appId": "1:604392656198:web:86deb1a323e4e57c696947",
    "measurementId": "G-SNRJHB8ENL"
}

# Inisialisasi database, auth, dan firebase untuk penggunaan selanjutnya
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()

def signIn(request):
    return render(request, "Login.html")

def postsignIn(request):
    email = request.POST.get('email')
    pasw = request.POST.get('pass')
    try:
        # Jika tidak ada kesalahan, masuklah pengguna dengan email dan kata sandi yang diberikan
        user = auth.sign_in_with_email_and_password(email, pasw)
    except:
        message = "Invalid Credentials! Please Check your Data"
        return render(request, "Login.html", {"message": message})
    
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    
    # Arahkan ke halaman beranda aplikasi dashboard
    return redirect('dashboard:home')

def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    return render(request, "Login.html")
