import os

def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(32)

    from hashlib import pbkdf2_hmac
    return salt + pbkdf2_hmac('sha256', password.encode(), salt, 100000)

def check_password(password, hash):
    return hash_password(password, hash[:32]) == hash



from main import mutation, redis_client

@mutation.field('login')
def resolve_login(*_, password, otp, expire=None):
    admin_hash = redis_client.get('admin.hash')
    admin_totp = redis_client.get('admin.totp')

    is_password_valid = check_password(password, admin_hash)
    is_otp_valid = True# pyotp.TOTP(admin_totp).verify(otp)
    if not is_password_valid or not is_otp_valid:
        raise Exception('Invalid password or OTP.')

    import time
    now = int(time.time())
    payload = { 'iss': issuer, 'iat': now }
    if expire is not None:
        payload['exp'] = now + expire
    
    import jwt
    issuer = 'pwnmachine'
    secret = os.urandom(32)
    token = jwt.encode(payload, secret)
    redis_client.set(f'admin.tokens.{token}', '*', expire)
    return { 'token': token, 'expire': payload.get('exp') }


@mutation.field('register')
def resolve_register(*_, password, otp):
    redis_client.set('admin.hash', hash_password(password))
    redis_client.set('admin.totp', otp)

from warnings import warn
warn('REMOVE DEFAULT PASSWORD AND TOTP')
resolve_register(password='admin', otp='W7RPT7JWR6YNSVOB')
