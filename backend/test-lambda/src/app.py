import json
import os
import pymysql
import boto3
import configparser


ENV_TYPE = os.getenv('envType', 'LOCAL')
config_file = "config.ini"

config = configparser.ConfigParser()
config.read(config_file)

session = boto3.Session(
    aws_access_key_id=config.get(ENV_TYPE, 'AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=config.get(ENV_TYPE, 'AWS_SECRET_ACCESS_KEY'),
    region_name= config.get(ENV_TYPE, 'REGION_NAME')
)

def lambda_handler(event, context):
    dbconn = pymysql.connect(
        user=config.get(ENV_TYPE, 'DBUSER'), 
        passwd=config.get(ENV_TYPE, 'DBPASSWD'), 
        host=config.get(ENV_TYPE, 'DBHOST'), 
        db=config.get(ENV_TYPE, 'DBNAME'), 
        charset=config.get(ENV_TYPE, 'DBCHARSET')
    )

    cursor = dbconn.cursor(pymysql.cursors.DictCursor)
    print('conn success.')

    sql = "SELECT prpt_his_id, gen_eng_cd, prpt, result FROM prompt_history order by prpt_his_id desc limit 1;"
    cursor.execute(sql)
    tmp_result = cursor.fetchall()

    result = {
        "prpt_his_id": tmp_result[0]['prpt_his_id'],
        "gen_eng_cd": tmp_result[0]['gen_eng_cd'],
        "prpt": tmp_result[0]['prpt'],
        "result": json.loads(tmp_result[0]['result'])
    }

    dbconn.close()
    
    return  {
        "statusCode": 200,
        "body": result,
        "headers": {
            "Content-Type": "application/json"
        }
    }
