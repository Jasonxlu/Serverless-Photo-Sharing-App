# insert follower and followee in followers table

import json
import os
import datatier

from configparser import ConfigParser

def lambda_handler(event, context):

    try:
        print("**STARTING**")
        print("**lambda: follow**")

        #
        # setup AWS based on config file:
        #
        config_file = 'config.ini'
        os.environ['AWS_SHARED_CREDENTIALS_FILE'] = config_file
        
        configur = ConfigParser()
        configur.read(config_file)
        
        #
        # configure for RDS access
        #
        rds_endpoint = configur.get('rds', 'endpoint')
        rds_portnum = int(configur.get('rds', 'port_number'))
        rds_username = configur.get('rds', 'user_name')
        rds_pwd = configur.get('rds', 'user_pwd')
        rds_dbname = configur.get('rds', 'db_name')

        
        #
        # get follower and followee parameters from event
        #
        print("**Accessing event/queryStringParameters**")
        
        if "queryStringParameters" in event:
            if "follower" in event["queryStringParameters"]:
                follower = event["queryStringParameters"]["follower"]
            else:
                
                raise Exception("requires follower parameter in queryStringParameters")
        else:
            raise Exception("requires follower query param")
            
        
            
        print("follower:", follower)

        if "queryStringParameters" in event:
            if "followee" in event["queryStringParameters"]:
                followee = event["queryStringParameters"]["followee"]
            else:
                raise Exception("requires followee parameter in queryStringParameters")
        else:
            raise Exception("requires followee query param")
            
        print("followee:", followee)


        dbConn = datatier.get_dbConn(rds_endpoint, rds_portnum, rds_username, rds_pwd, rds_dbname)
        sql = 'SELECT * FROM users WHERE userid = %s OR userid = %s'
        users_exist = datatier.retrieve_all_rows(dbConn, sql, [follower, followee])
        if len(users_exist) < 2:
            print('Error: Cannot follow nonexistent user') # if user tries to follow someone that doesn't exist
            return {
                'statusCode': 400,
                'headers': {
        'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
                'body': 'Cannot follow nonexistent user'
            }

        sql = 'SELECT followeeid FROM followers WHERE followerid = %s and followeeid = %s'
        exists = datatier.retrieve_one_row(dbConn, sql, [follower, followee])
        if len(exists) == 0: # follower-followee connection doesn't already exist (if already exists, do nothing)
            sql = 'INSERT INTO followers (followerid, followeeid) values (%s, %s)'
            datatier.perform_action(dbConn, sql, [follower, followee])
            print('user', follower, 'now follows user', followee)
        


        return {
            'statusCode': 200,
            'headers': {
        'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
            'body': 'success'
        }

    except Exception as e:
        print("**ERROR**")
        print(str(e))
    
        return {
        'statusCode': 400,
        'headers': {
        'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
        'body': json.dumps(str(e))
        }