#!/usr/bin/python
# marek kuczynski
# @marekq
# www.marek.rocks
# coding: utf-8

# import neccesary libraries
from boto3 import resource
import botocore.vendored.requests as requests
from os import environ
from datetime import datetime, timedelta
import urllib3

# set up connections with cognito and dynamodb using boto3
dynamo  = resource('dynamodb').Table(environ['dynamotable'])

# get the outbound ip address of the lambda function
http 	= urllib3.PoolManager()
ip 		= http.request('GET', 'http://ipinfo.io/ip').data.decode("utf-8")

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

	# parse the html output
	body            = '<html>'+open('./head.css').read()
	body 		 	+= '<body><center><div><br>'
	body 			+= '<p><b>region '+str(environ['AWS_REGION'])+' &#8226; '
	body 			+= 'ip '+str(ip)+' &#8226; '
	body 			+= 'uptime '+str(uptime_string)+'</p></b><br>'
	body            += str(b)
	body            += '</div></center></body></html>'
	resp['body']    = body

	# return a http 200 response code
	return resp

# scans the messages in dynamodb
def get_messages():
	# scan all messages in the table
	x           = dynamo.scan()
	l           = len(x['Items'])
	r           = []

	# print the username, timestamp and message 
	for y in range(l):
		usr     = str(x['Items'][y]['user'])
		msg     = str(x['Items'][y]['message'])
		tim     = x['Items'][y]['timest']
		dat 	= datetime.utcfromtimestamp(int(tim)).strftime('%Y-%m-%d %H:%M:%S')

		r.append('<tr><td>'+usr+'</td><td>'+str(dat)[5:16]+'</td><td>'+msg +'</td></tr>')

	# return the html content
	return r

# return html for GET users request
def get_table(msg):
	body        = '<center><table width = 100%><tr><th>user</th><th>date</th><th>message</th></tr><tr>'

	for x in msg:
		body    += x

	body        += '</table></center>'

	return body
	
# lambda handler
def handler(event, context):
	# handle GET requests by returning an HTML page
 
	msg     = get_messages()
	tab     = get_table(msg)
	html    = return_html(tab)

	return html
