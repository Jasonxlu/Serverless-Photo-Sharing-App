# insert user in users table

import json
import os
import datatier

from configparser import ConfigParser

def lambda_handler(event, context):


    try:
        print("**STARTING**")
        print("**lambda: add_user**")
        
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
        # get username parameter from event
        #
        print("**Accessing event/pathParameters**")

        if "uname" in event:
            uname = event["uname"]
        elif "pathParameters" in event:
            if "uname" in event["pathParameters"]:
                uname = event["pathParameters"]["uname"]
            else:
                raise Exception("requires uname parameter in pathParameters")
        else:
            raise Exception("requires uname parameter in event")
            
        print("uname:", uname)

        dbConn = datatier.get_dbConn(rds_endpoint, rds_portnum, rds_username, rds_pwd, rds_dbname)
        sql = 'SELECT * FROM users WHERE username = %s'
        exists = datatier.retrieve_one_row(dbConn, sql, [uname])
        if len(exists) > 0:
            print('Error: User not created, username', uname, 'already exists')
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps('User already exists')
                
                
            }
        
        sql = 'INSERT INTO users (username) values (%s)'
        userid = datatier.perform_action(dbConn, sql, [uname])
        print('user', uname, 'inserted with userid', userid)
        
        # Get the userid
        sql = 'Select userid from users where username = %s'
        userid = datatier.retrieve_one_row(dbConn, sql, [uname])
        print('New userid queried: ', userid)

        return {
            'statusCode': 200,
            'headers': {
                    'Access-Control-Allow-Origin': '*',
                },
            'body': json.dumps({'status': 'success', 'userid': userid})
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


def test_func(uname):
    print("**STARTING**")
    print("**lambda: add_user**")

    
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
    sql = 'SELECT * FROM users WHERE username = %s'
    exists = datatier.retrieve_one_row(dbConn, sql, [uname])
    if len(exists) > 0:
        print('Error: user not created, username', uname, 'already exists')
        return
    
    sql = 'INSERT INTO users (username) values (%s)'
    userid = datatier.perform_action(dbConn, sql, [uname])
    print('user', uname, 'inserted with userid', userid)


test_func('chillax')
test_func('imanewuser')

