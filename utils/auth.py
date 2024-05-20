# authentication/utils/auth.py

from firebase_admin import auth as admin_auth

def verify_id_token(token):
    try:
        # Verifikasi token menggunakan Firebase Admin SDK
        decoded_token = admin_auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        print(f"Error verifying ID token: {e}")
        return None

def revoke_token(uid):
    try:
        # Mencabut token menggunakan Firebase Admin SDK
        admin_auth.revoke_refresh_tokens(uid)
    except Exception as e:
        print(f"Error revoking tokens: {e}")
