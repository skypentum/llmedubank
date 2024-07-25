import json
import time
import pymysql
import os
import configparser

ENV_TYPE = os.getenv('envType', 'LOCAL')
config_file = "config.ini"

config = configparser.ConfigParser()
config.read(config_file)


def insert_question_answer_history(data, dbconn, cursor):
    for row in data['questionHis']:
        row['qstHisId'] = int(time.time()) 
        
        sql = f'''
        insert into question_answer_history (qst_his_id, usr_id, std_cnt, qst_id, answer, crrct_yn, crt_at)
        values ({row['qstHisId']}, '{row['usrId']}', {row['stdCnt']}, {row['qstId']}, '{row['answer']}', '{row['crrctYn']}', now())  
        '''
        cursor.execute(sql)
        # unix time key 중복 생성으로 인해 1초 간격으로 저장하도록 sleep 구성(추후 개선 필요.)
        time.sleep(1)
    dbconn.commit()


def lambda_handler(event, context):    
    dbconn = pymysql.connect(
        user=config.get(ENV_TYPE, 'DBUSER'), 
        passwd=config.get(ENV_TYPE, 'DBPASSWD'), 
        host=config.get(ENV_TYPE, 'DBHOST'), 
        db=config.get(ENV_TYPE, 'DBNAME'), 
        charset=config.get(ENV_TYPE, 'DBCHARSET')
    )
    cursor = dbconn.cursor(pymysql.cursors.DictCursor)

    insert_question_answer_history(event, dbconn, cursor)        
    dbconn.close()
    
    return json.dumps({
        'status': 200,
        'message': 'success'
    })
