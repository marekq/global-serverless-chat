import boto3, sys, time

ddb     = boto3.client('dynamodb')
ts      = str(int(time.time()))
user    = 'marek'
msg	= sys.argv[1]


def push():
    ddb.put_item(TableName = 'geochat', 
	Item = {
	    'timest'	: {"S": ts } ,
	    'message'	: {"S": msg},
        'user'      : {"S": user }
	})

    print('added item '+msg+' from user '+user)

push()
