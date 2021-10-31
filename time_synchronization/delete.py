import hmac
import base64
import struct
import hashlib
import time

SECRET_KEY = 'MNUGC2DBGBZQ===='

def get_totp_token():
	# sleep 30 sec
    interval = int(time.time()) // 30
    key = base64.b32decode(SECRET_KEY, True)
    message = struct.pack(">Q", interval)
    hashh = hmac.new(key, message, hashlib.sha1).digest()
    index = hashh[19] & 15
    result = (struct.unpack(">I", hashh[index:(index + 4)])[0] & 0x7fffffff) % 1000000
    return str(result)

print(get_totp_token())
