from flask import *

app = Flask(__name__)
app.secret_key = 'otp'

@app.route('/')
def home():
	return render_template('login.html')


def getOTP_TOKEN(s: str):
	# прямой полиномиальный хэш
	# алфавит из 28 букв
	k = 31
	mod = 1e9+7
	h = 0
	m = 1
	for c in s:
		x = int(ord(c) - ord('a') + 1)
		h = (h + m * x) % mod
		m = (m * k) % mod 
	return str(int(h))


@app.route('/getOTP', methods=['POST'])
def getOTP():
	login = request.form['login']
	password = request.form['password']

	otp = getOTP_TOKEN(password)
	with open('OTP.txt', 'w') as f:
		f.write('Your OTP: ' + str(otp))

	session['login'] = str(login)
	session['otp'] = str(otp)

	return render_template('login.html')


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
		else:
			ret_value += 'not logined in'

		return ret_value


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5002, debug=True)