from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings  
from utils.auth import verify_id_token, revoke_token  
import time  
import pyrebase

# Inisialisasi konfigurasi Firebase dari settings.py
firebase_config = settings.FIREBASE_CONFIG

# Inisialisasi Firebase
firebase = pyrebase.initialize_app(firebase_config)
auth_pyrebase = firebase.auth()
database = firebase.database()

def signIn(request):
    time.sleep(3)
    if 'uid' in request.session:
        token = request.session['uid']
        decoded_token = verify_id_token(token)
        if decoded_token:
            return redirect('dashboard:home')
    return render(request, "Login.html")


def postsignIn(request):
    email = request.POST.get('email')
    pasw = request.POST.get('pass')
    try:
        user = auth_pyrebase.sign_in_with_email_and_password(email, pasw)
    except:
        messages.error(request, "Invalid Credentials! Please check your data.")
        return redirect('authentication:login')
    
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    
    return redirect('dashboard:home')


def logout(request):
    try:
        token = request.session['uid']
        decoded_token = verify_id_token(token)
        uid = decoded_token.get('uid')
        revoke_token(uid)
        del request.session['uid']
    except KeyError:
        pass
    return redirect('authentication:login')
