from flask import *
import hmac
import base64
import struct
import hashlib
import time

SECRET_KEY = 'ABCDEFGHIJKLMNOP'
USERS = {}

app = Flask(__name__)
app.secret_key = 'otp'

@app.route('/')
def home():
	return render_template('login.html')

def getOTP_TOKEN(login):
	# Event-based OTP (with HOTP)
    interval = int(time.time()) // 30
    key = base64.b32decode(SECRET_KEY, True)

    i = USERS.get(login, 0)
    result = bytearray()
    while i != 0:
        result.append(i & 0xFF)
        i >>= 8
    message = bytes(bytearray(reversed(result)).rjust(8, b'\0'))
    
    hashh = hmac.new(key, message, hashlib.sha1).digest()
    index = hashh[19] & 15
    result = (struct.unpack(">I", hashh[index:(index + 4)])[0] & 0x7fffffff) % 1000000
    
    return str(result)


@app.route('/getOTP', methods=['POST'])
def getOTP():
	login = request.form['login']
	password = request.form['password']

	otp = getOTP_TOKEN(login)

	# only for user
	with open('OTP.txt', 'w') as f:
		f.write('Отдельно подсчитываем OTP с помощью количества прохождения аутентификации.\nYour OTP: ' + str(otp))

	session['login'] = str(login)
	session['otp'] = str(otp)

	return render_template('OTP.html')


@app.route('/validateOTP', methods=['POST'])
def validateOTP():
	otp = request.form['otp']
	if 'otp' in session:
		login = session['login']
		session.pop('login', None)

		s = session['otp']
		session.pop('otp', None)

		ret_value = 'User ' + login + ' are '
		if s == otp:
			ret_value += 'logined in'
			USERS[login] = USERS.get(login, 0) + 1
		else:
			ret_value += 'not logined in'

		return ret_value


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5002, debug=True)