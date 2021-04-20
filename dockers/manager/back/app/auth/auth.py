import os
import time
import argon2
import pyotp
import jwt
from warnings import warn
from ..utils.registration import registerMutation, registerQuery, createType
from ..redis import client as redis_client

hasher = argon2.PasswordHasher()
issuer = 'pwnmachine'


SECRET = os.urandom(32)

@registerMutation('login')
def resolve_login(*_, password, otp, expire=None):
    admin_hash = redis_client.get('admin.hash')
    admin_totp = redis_client.get('admin.totp')

    try:
        hasher.verify(admin_hash, password)
    except:
        raise Exception('Invalid password')
    if not pyotp.TOTP(admin_totp).verify(otp):
        raise Exception('Invalid OTP')

    now = int(time.time())
    payload = { 'iss': issuer, 'iat': now }
    if expire is not None:
        payload['exp'] = now + expire
    
    token = jwt.encode(payload, secret)
    redis_client.set(f'admin.tokens.{token}', '*', expire)
    return { 'token': token, 'expire': payload.get('exp') }

@registerMutation('register')
def resolve_register(*_, password, otp):
    admin_totp = redis_client.get('admin.totp')
    if not pyotp.TOTP(admin_totp).verify(otp):
        raise Exception('Invalid OTP')
    redis_client.set('admin.hash', hasher.hash(password))

#warn('REMOVE DEFAULT PASSWORD AND TOTP')
#redis_client.set('admin.totp', 'W7RPT7JWR6YNSVOB')
#redis_client.set('admin.hash', hasher.hash('admin'))
