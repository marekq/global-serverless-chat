#!/usr/bin/python
# marek kuczynski
# @marekq
# www.marek.rocks
# coding: utf-8

# import neccesary libraries
import base64, time, urllib3

from boto3 import client
from os import environ
from re import search
from urllib.parse import unquote

# set up connections with cognito and dynamodb using boto3
ddb  	= client('dynamodb')
cmp  	= client('comprehend')
http 	= urllib3.PoolManager()

# return 301 redirect
def get_html_301(surl):
	resp = {
		"statusCode": 301,
		"headers": {
			"Content-Type": "text/html",
			"Location": str(surl)
		}
	}

	return resp

# check if the message does not contain negative text 
def write_msg(user, msg, ipuser, ipcountry):

	# check the username and text using comprehend 
	x 		= cmp.detect_sentiment(Text = str(user)+' '+str(msg), LanguageCode = 'en')['Sentiment']
	
	# if the message is not classified as negative, write it to DynamoDB
	if x != 'NEGATIVE':
		ts 	= str(int(time.time()))

		try:
			ddb.put_item(TableName = environ['dynamotable'], 
			Item = {
				'timest'    : {"S": ts},
				'user'      : {"S": str(user)},
				'message'   : {"S": str(msg).replace('+', ' ')},
				'ip'		: {"S": str(ipuser)},
				'country'	: {"S": str(ipcountry)}
			})

			print('### added item '+msg+' from user '+user+' to dynamodb')

		except Exception as e:
			print('### failed to add record to ddb with user '+str(user)+', error '+str(e))
	else:
		print('### not added text due to negative score, user: '+str(user)+', message: '+str(msg))

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

# lambda handler for the http request
def handler(event, context):

	# handle GET requests by returning an HTML page
	para 		= event['body']

	# get the requester ip
	ipu 		= str(event['requestContext']['identity']['sourceIp'])

	# lookup the users country
	ipc 		= http.request('GET', 'https://ipinfo.io/'+ipu+'/country').data.decode("utf-8").strip()

	# get the haders from the file and decode them
	p 			= base64.b64decode(para).decode("utf-8")
	user, msg 	= get_header(str(p))
	print('&&& found user '+str(user)+' message '+str(msg))
	
	# write the message to DynamoDB
	if len(user) != 0 and len(msg) != 0:
		# if localhost is submitting (i.e. sam local), set the country to NL
		if ipu == '127.0.0.1':
			ipc = 'NL'

		# if the country is unknown, set to '??'
		elif len(ipc) == 0:
			ipc = '??'

		write_msg(user, msg, ipu, ipc)
		print('wrote message '+msg+' from user '+user)

	# return a 301 redirect back go the original page
	retpa	= event['path']
	html 	= get_html_301(retpa.replace('home', 'Prod/home'))

	return html
