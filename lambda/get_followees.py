# get all followees of the user from the followers table

import json
import os
import datatier

from configparser import ConfigParser

def lambda_handler(event, context):
    try:
        print("**STARTING**")
        print("**lambda: get_followees**")
        
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
        # get follower parameter from event
        #
        print("**Accessing event/pathParameters**")

        if "follower" in event:
            follower = event["follower"]
        elif "pathParameters" in event:
            if "follower" in event["pathParameters"]:
                follower = event["pathParameters"]["follower"]
            else:
                raise Exception("requires follower parameter in pathParameters")
        else:
            raise Exception("requires follower parameter in event")
            
        print("follower:", follower)

        dbConn = datatier.get_dbConn(rds_endpoint, rds_portnum, rds_username, rds_pwd, rds_dbname)
        sql = '''
        SELECT users.username FROM followers LEFT JOIN users ON followers.followeeid = users.userid WHERE followerid = %s 
        '''
        results = datatier.retrieve_all_rows(dbConn, sql, [follower])

        followers = [x[0] for x in results]
        print(followers)
        
        return {
            'statusCode': 200,
            'body': json.dumps(followers),
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


