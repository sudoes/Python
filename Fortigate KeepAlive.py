#Author: HafizJef
#Usage: Python [scriptname.py]

import time, requests
from datetime import datetime

baseurl = 'http://172.16.1.254:1000/'
url = 'http://gstatic.com'
cutStart = 'keepalive?'
cutEnd = '";'
user = 'id'
passw = 'pass'

def now():
	clock = datetime.now()
	return clock.strftime('%H:%M:%S')


def getLogin():
	global login
	r = requests.get(url)
	print ('(%s) [REQ] %s' % (now(), r.url))
	login = r.url
	mainProc()

def keepAlive(authCode):
	while True:
		kaUrl = 'http://172.16.1.254:1000/keepalive?' + authCode
		print ('(%s) [ACK] %s -' % (now(), authCode)),
		getKa = requests.get(kaUrl)
		print (getKa.status_code)
		time.sleep(99)

def mainProc():
	if 'auth' in login:
		magic = login.split('?')[1]
		payload = {'magic': magic, 'username': user, 'password': passw, '4Tredirect': url}
		p = requests.post(baseurl, data=payload)
		lgdata = p.text
		authCode =  lgdata[(lgdata.index(cutStart)+len(cutStart)):lgdata.index(cutEnd)]
		keepAlive(authCode)

	else:
		print ('(%s) No Redirect, Retrying...' % (now()))
		getLogin()

getLogin()

#print '(%s) [DBG] %s' % (now(), login)









