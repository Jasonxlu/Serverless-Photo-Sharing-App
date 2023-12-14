# get all userids and usernames from users table

import json
import os
import datatier

from configparser import ConfigParser

def lambda_handler(event, context):
    try:
        print("**STARTING**")
        print("**lambda: get_users**")
        
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

        dbConn = datatier.get_dbConn(rds_endpoint, rds_portnum, rds_username, rds_pwd, rds_dbname)
        sql = 'SELECT * FROM users ORDER BY userid'
        results = datatier.retrieve_all_rows(dbConn, sql)

        print("**DONE, returning userids and usernames**")

        # json response goes here
        return {
            'statusCode': 200,
            'body': json.dumps(results),
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



    