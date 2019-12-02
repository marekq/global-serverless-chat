import boto3, sys, time

ddb     = boto3.client('dynamodb')
user    = 'marek'
ip 	 	= '127.0.0.1'
country = 'NL'

def push(msg):
	ts      = str(int(time.time()))

	ddb.put_item(TableName = 'geochat', 
	Item = {
	    'timest'	: {"S": ts} ,
	    'message'	: {"S": msg },
        'user'      : {"S": user },
		'country'	: {"S": country },
		'ip' 		: {"S": ip }
	})

	print('added item '+msg+' from user '+user)

c  	= 1

for x in range(100):
	c  		+= 1
	ts      = str(int(time.time()))
	
	print(str(c)+' message '+str(ts))
	time.sleep(1)

	push(ts)
