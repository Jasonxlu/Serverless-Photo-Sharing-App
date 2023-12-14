# inserts post info in posts table, uploads image to s3


import json
import boto3
import os
import uuid
import base64
import pathlib
import datatier
from datetime import datetime

from configparser import ConfigParser

def lambda_handler(event, context):
    try:
        print("**STARTING**")
        print("**lambda: post_image**")
        
        #
        # setup AWS based on config file:
        #
        config_file = 'config.ini'
        os.environ['AWS_SHARED_CREDENTIALS_FILE'] = config_file
        
        configur = ConfigParser()
        configur.read(config_file)
        
        #
        # configure for S3 access:
        #
        s3_profile = 's3readwrite'
        boto3.setup_default_session(profile_name=s3_profile)
        
        bucketname = configur.get('s3', 'bucket_name')
        
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucketname)
        
        #
        # configure for RDS access
        #
        rds_endpoint = configur.get('rds', 'endpoint')
        rds_portnum = int(configur.get('rds', 'port_number'))
        rds_username = configur.get('rds', 'user_name')
        rds_pwd = configur.get('rds', 'user_pwd')
        rds_dbname = configur.get('rds', 'db_name')
        
        #
        # userid from event: could be a parameter
        # or could be part of URL path ("pathParameters"):
        #
        print("**Accessing event/pathParameters**")
    
        if "userid" in event:
            userid = event["userid"]
        elif "pathParameters" in event:
            if "userid" in event["pathParameters"]:
                userid = event["pathParameters"]["userid"]
            else:
                raise Exception("requires userid parameter in pathParameters")
        else:
            raise Exception("requires userid parameter in event")
            
        print("userid:", userid)
    
        #
        # the user has sent us two parameters:
        #  1. filename of their file
        #  2. raw file data in base64 encoded string
        #
        # The parameters are coming through web server 
        # (or API Gateway) in the body of the request
        # in JSON format.
        #
        print("**Accessing request body**")
        
        if "body" not in event:
            raise Exception("event has no body")
        
        body = json.loads(event["body"]) # parse the json
        
        if "filename" not in body:
            raise Exception("event has a body but no filename")
        if "data" not in body:
            raise Exception("event has a body but no data")

        filename = body["filename"]
        datastr = body["data"]
        caption = ''
        
        if 'caption' in body:
            caption = body['caption']
        
        print("filename:", filename)
        print("datastr (first 10 chars):", datastr[0:10])

        #
        # open connection to the database:
        #
        print("**Opening connection**")
        
        dbConn = datatier.get_dbConn(rds_endpoint, rds_portnum, rds_username, rds_pwd, rds_dbname)

        #
        # first we need to make sure the userid is valid:
        #
        print("**Checking if userid is valid**")
        
        sql = "SELECT username FROM users WHERE userid = %s;"
        
        row = datatier.retrieve_one_row(dbConn, sql, [userid])
        
        if row == ():  # no such user
            print("**No such user, returning...**")
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps("no such user...")
            }
        
        username = row[0]
        
        #
        # at this point the user exists, so safe to upload to S3:
        #
        base64_bytes = datastr.encode()        # string -> base64 bytes
        bytes = base64.b64decode(base64_bytes) # base64 bytes -> raw bytes
        
        #
        # write raw bytes to local filesystem for upload:
        #
        print("**Writing local data file**")
        
        local_filename = "/tmp/data.pdf"
        
        outfile = open(local_filename, "wb")
        outfile.write(bytes)
        outfile.close()
        
        #
        # generate unique filename in preparation for the S3 upload:
        #
        print("**Uploading local file to S3**")
        
        basename = pathlib.Path(filename).stem
        extension = pathlib.Path(filename).suffix
        
        if extension != ".jpg" : 
            raise Exception("expecting filename to have .jpg extension")
        
        bucketkey = "photo-media-app-jackebs/" + username + "/" + basename + "-" + str(uuid.uuid4()) + ".jpg"
        
        print("S3 bucketkey:", bucketkey)
        
        #
        # add a jobs record to the database BEFORE we upload, just in case
        # the compute function is triggered faster than we can update the
        # database:
        #
        print("**Adding posts row to database**")
        
        sql = """
            INSERT INTO posts(posterid, bucketkey, caption)
                    VALUES(%s, %s, %s);
        """
        
        datatier.perform_action(dbConn, sql, [userid, bucketkey, caption])
        
        #
        # grab the jobid that was auto-generated by mysql:
        #
        sql = "SELECT LAST_INSERT_ID();"
        
        row = datatier.retrieve_one_row(dbConn, sql)
        
        postid = row[0]
        
        print("uploaded post with id (postid):", postid)
        
        #
        # finally, upload to S3:
        #
        print("**Uploading data file to S3**")

        bucket.upload_file(local_filename, 
                    bucketkey, 
                    ExtraArgs={
                        'ACL': 'public-read',
                        'ContentType': 'image/jpeg'
                    })

        #
        # respond in an HTTP-like way, i.e. with a status
        # code and body in JSON format:
        #
        print("**DONE, returning postid**")
        
        return {
            'statusCode': 200,
            'headers': {
                    'Access-Control-Allow-Origin': '*',
                },
            'body': json.dumps(str(postid))
        }
        
    except Exception as err:
        print("**ERROR**")
        print(str(err))
        
        return {
            'statusCode': 400,
            'headers': {
                    'Access-Control-Allow-Origin': '*',
                },
            'body': json.dumps(str(err))
        }
