# delete follower-followee row from followers table

import json
import os
import datatier

from configparser import ConfigParser

def lambda_handler(event, context):
    try:
        print("**STARTING**")
        print("**lambda: unfollow**")

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

        if "follower" in event:
            follower = event["follower"]
        elif "queryStringParameters" in event:
            if "follower" in event["queryStringParameters"]:
                follower = event["queryStringParameters"]["follower"]
            else:
                raise Exception("requires follower parameter in queryStringParameters")
        else:
            raise Exception("requires follower parameter in event")
            
        print("follower:", follower)

        if "followee" in event:
            followee = event["followee"]
        elif "queryStringParameters" in event:
            if "followee" in event["queryStringParameters"]:
                followee = event["queryStringParameters"]["followee"]
            else:
                raise Exception("requires followee parameter in queryStringParameters")
        else:
            raise Exception("requires followee parameter in event")
            
        print("followee:", followee)

        dbConn = datatier.get_dbConn(rds_endpoint, rds_portnum, rds_username, rds_pwd, rds_dbname)
        sql = 'SELECT followeeid FROM followers WHERE followerid = %s and followeeid = %s'
        exists = datatier.retrieve_one_row(dbConn, sql, [follower, followee])
        if len(exists) > 0: # follower-followee connection exists (otherwise do nothing)
            sql = 'DELETE FROM followers where followerid = %s and followeeid = %s'
            datatier.perform_action(dbConn, sql, [follower, followee])
            print('user', follower, 'no longer follows user', followee)
        
            return {
                'statusCode': 200,
                'body': 'success',
                'headers': {
                    'Access-Control-Allow-Origin': '*'  # Replace * with your allowed origin(s)
                    # Add other CORS headers if needed, e.g., 'Access-Control-Allow-Methods', etc.
                }
            }

    except Exception as e:
        print("**ERROR**")
        print(str(e))
    
        return {
            'statusCode': 400,
            'body': json.dumps(str(e)),
            'headers': {
                'Access-Control-Allow-Origin': '*'  # Replace * with your allowed origin(s)
                # Add other CORS headers if needed, e.g., 'Access-Control-Allow-Methods', etc.
            }
        }
