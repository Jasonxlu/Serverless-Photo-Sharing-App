# get all followees of the user from the followers table

import json
import os
import datatier

from configparser import ConfigParser

def lambda_handler(event, context):
    try:
        print("**STARTING**")
        print("**lambda: lookup_user**")
        
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
        # get userid parameter from event
        #
        print("**Accessing event/pathParameters**")

        if "uname" in event:
            username = event["uname"]
        elif "pathParameters" in event:
            if "uname" in event["pathParameters"]:
                username = event["pathParameters"]["uname"]
            else:
                raise Exception("requires username parameter in pathParameters")
        else:
            raise Exception("requires username parameter in event")
            
        print("username:", username)

        dbConn = datatier.get_dbConn(rds_endpoint, rds_portnum, rds_username, rds_pwd, rds_dbname)
        sql = '''
        SELECT userid FROM users WHERE username=%s 
        '''
        results = datatier.retrieve_one_row(dbConn, sql, [username])
        
        if len(results) == 0:
            print("no users found")
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps("No user found")
            }

        userid_rtn = results[0]
        print(userid_rtn)
        
        return {
            'statusCode': 200,
            'headers': {
                    'Access-Control-Allow-Origin': '*',
                },
            'body': json.dumps(str(userid_rtn))
        }

    except Exception as e:
        print("**ERROR**")
        print(str(e))
    
        return {
        'statusCode': 400,
        'headers': {
                    'Access-Control-Allow-Origin': '*',
                },
        'body': json.dumps(str(e))
        }

