# get all posts by the user and their followers from the posts table, ordered by most to least recent
# download those post images from s3, turn that into the base 64 whatever to return to the client


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
        print("**lambda: get_feed**")
        
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
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps("no such user...")
            }  

        sql = '''
        SELECT posts.postid, users.username, posts.bucketkey, posts.caption
        FROM posts
        LEFT JOIN followers ON followers.followeeid = posts.posterid AND followers.followerid = %s
        LEFT JOIN users ON users.userid = posts.posterid
        WHERE followers.followerid IS NOT NULL OR posts.posterid = %s
        ORDER BY posts.tmstmp DESC;
        '''

        posts = datatier.retrieve_all_rows(dbConn, sql, [userid, userid])
        
        
        print("**DONE, returning results**")
        
        return {
            'statusCode': 200,
            'headers': {
                    'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(posts)
        }
        
    except Exception as err:
        print("**ERROR**")
        print(str(err))
        
        return {
            'statusCode': 400,
            'headers': {
        'Access-Control-Allow-Origin': '*'
    },
            'body': json.dumps(str(err))
        }
    
