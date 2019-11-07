#!/usr/bin/python
# marek kuczynski
# @marekq
# www.marek.rocks
# coding: utf-8

# import neccesary libraries
import boto3
from os import environ
from time import time
from datetime import datetime, timedelta

# set up connections with cognito and dynamodb using boto3
dynamo  = boto3.resource('dynamodb').Table(environ['dynamotable'])

# return html with a 200 code
def return_html(b):
	
	resp = {
		"statusCode": 200,
		"headers": {
			"Content-Type": "text/html"
		}
	}

	body            = '<html><body><center><br><h1>Welcome to the Global Serverless Chat demo!</h1>'
	body            += '<br><h2>This request is served from '+str(environ['AWS_REGION'])+'</h2><br>'
	body            += str(b)
	body            += '</center></body></html>'

	resp['body']    = body

	# return a http 200 response code
	return resp

# scans the messages in dynamodb
def get_messages():
	x           = dynamo.scan()
	l           = len(x['Items'])
	r           = []

	for y in range(l):
		usr     = str(x['Items'][y]['user'])
		msg     = str(x['Items'][y]['message'])
		tim     = x['Items'][y]['timest']
		dat 	= datetime.utcfromtimestamp(int(tim)).strftime('%Y-%m-%d %H:%M:%S')

		r.append('<tr><td>'+str(tim)+'</td><td>'+str(dat)+'</td><td>'+usr+'</td><td>'+msg +'</td></tr>')

	return r

# GET users
def get_table(msg):
	body        = '<table width = "800"><tr><th>unix timestamp</th><th>timestamp (utc)</th><th>user</th><th>message</th></tr><tr>'

	for x in msg:
		body    += x

	body        += '</table>'

	return body
	
# lambda handler
def handler(event, context):
	# handle GET requests by returning an HTML page
 
	msg     = get_messages()
	tab     = get_table(msg)
	html    = return_html(tab)

	return html
