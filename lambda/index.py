#!/usr/bin/python
# marek kuczynski
# @marekq
# www.marek.rocks
# coding: utf-8

# import neccesary libraries
import botocore.vendored.requests as requests
import time, urllib3

from boto3 import client
from datetime import datetime, timedelta
from os import environ, path
from struct import unpack
from socket import inet_aton
from re import search
from urllib.parse import unquote

# set up connections with cognito and dynamodb using boto3
ddb  = client('dynamodb')

# set a variable with the temporary ip file
ipfile 	= '/tmp/ip.txt'

# retrieve the external ip address of the lambda function
def get_ip():

	# check if the tempfile is in /tmp/ip.txt
	if path.isfile(ipfile):
		print('!!! found file '+ipfile)
		ip 		= open(ipfile).read()

	else:
		# get the outbound ip address of the lambda function
		print('!!! didnt find file '+ipfile)
		http 	= urllib3.PoolManager()
		ip 		= http.request('GET', 'http://ipinfo.io/ip').data.decode("utf-8").strip()

		# write the ip address to the /tmp/ip.txt file
		f 		= open(ipfile, 'w')
		f.write(ip)
		f.close

	return ip

# retrieve the ip as a global variable
ip 		= get_ip()

# convert an IP to a 6 character hex code that will be the background color
def ip2int(addr):
	return hex(unpack("!I", inet_aton(addr))[0] * 1000)[-6:]

# get the posted string username and message from the headers
def get_header(para):
	user, msg = '', ''

	print('@@@ '+str(para))

	# split the provided username and password
	if search('&', para):
		for y in para.split('&'):
			if search('username', y):
				user    = unquote(y[9:])
			elif search('message', y):
				msg    = unquote(y[8:])

	return user, msg

# return html with a 200 code
def return_html(b):
	
	# set the return html headers
	resp = {
		"statusCode": 200,
		"headers": {
			"Content-Type": "text/html"
		}
	}

	# get system uptime
	with open('/proc/uptime', 'r') as f:
		uptime_seconds = float(f.readline().split()[0])
		uptime_string = str(timedelta(seconds = uptime_seconds)).split('.')[0]

	# parse the html output, generate the background color of the page
	body            = '<html>'+open('./head.css').read().replace('%COLOR%', str(ip2int(ip)))
	body 		 	+= '<body><center><div><br>'
	body 			+= '<p><b>region '+str(environ['AWS_REGION'])+' &#8226; '
	body 			+= 'ip '+str(ip)+' &#8226; '
	body 			+= 'uptime '+str(uptime_string)+'</p></b><br>'
	body 	 		+= 'Welcome to the global serverless chat!<br><br>'
	body 			+=  '<form method = "post"> username <input type = "username" name = "username" />'
	body 			+= ' message <input type = "message" name = "message" />'
	body 			+= '<input type = "submit" /></form>'
	body            += str(b)
	body            += '</div></center></body></html>'
	resp['body']    = body

	# return a http 200 response code
	return resp

# scans the messages in dynamodb
def get_messages():
	# scan all messages in the table
	x           = ddb.scan(TableName = environ['dynamotable'])
	l           = len(x['Items'])
	r, t        = [], []

	# print the username, timestamp and message 
	for y in  sorted(range(l), reverse = True):
		usr     = str(x['Items'][y]['user']['S'])
		msg     = str(x['Items'][y]['message']['S'])
		tim     = str(x['Items'][y]['timest']['S'])

		# convert the unix ts to a string		
		dat 	= datetime.utcfromtimestamp(int(tim)).strftime('%Y-%m-%d %H:%M:%S')
		
		# get the time difference
		age 	= get_date(tim)
		t.append([tim, age, usr, msg])

	for y in sorted(t, reverse = True):
		r.append('<tr><td>'+y[2]+'</td><td>'+str(y[1])+'</td><td>'+str(y[3]) +'</td></tr>')

	# return the html content
	return r

# return html for GET users request
def get_table(msg):
	body        = '<center><table width = 100%><tr><th>user</th><th>age</th><th>message</th></tr><tr>'

	for x in msg:
		body    += x

	body        += '</table></center>'

	return body

# determine how old the chat message is  
def get_date(x):
	y		= time.time()
	z		= int(y) - int(x)
	
	years	= str(int(int(z)/31536000))
	months	= str(int(int(z)/2592000))
	weeks	= str(int(int(z)/604800))
	days	= str(int(int(z)/86400))
	hours	= str(int(int(z)/3600) % 24)
	mins 	= str(int(int(z)/60) % 3600)
	secs 	= str(int(int(z)) % 60)

	if hours == str('0') and z < 60:
		return secs+'s'

	elif hours == str('0') and z < 3600:
		return mins+'m'

	elif hours != str('0') and z < 86400:
		return hours+'h'

	elif int(days) < int(31):
		return days+'d'

	elif int(days) < int(365):
		return weeks+'w'

	else:
		return years+'y'

def write_msg(user, msg):
	ts      = str(int(time.time()))

	try:
		ddb.put_item(TableName = environ['dynamotable'], 
		Item = {
			'timest'    : {"S": ts},
			'user'      : {"S": str(user)},
			'message'   : {"S": str(msg)}
		})

		print('### added item '+msg+' from user '+user+' to dynamodb')

	except Exception as e:
		print('### failed to add record to ddb, error '+str(e))

# lambda handler for the http request
def handler(event, context):
	user, msg 	= '', ''

	try:
		meth 	= str(event['httpMethod'])
	except:
		meth 	= ''

	# handle GET requests by returning an HTML page
	if meth == 'POST':
		para 		= event['body']
		user, msg 	= get_header(para)
		print('&&& found user '+str(user)+' message '+str(msg))
	
	# if strings are submitted, post the message
	if len(user) != 0 and len(msg) != 0:
		write_msg(user, msg)

	msg     	= get_messages()
	tab     	= get_table(msg)
	html    	= return_html(tab)

	return html
