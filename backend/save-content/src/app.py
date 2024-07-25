import os
import pymysql
import configparser

ENV_TYPE = os.getenv('envType', 'LOCAL')
config_file = "config.ini"

config = configparser.ConfigParser()
config.read(config_file)
    

def insert_content(data, dbconn, cursor):       
    sql = f'''
    insert into define_meta (prpt_his_id, gen_eng_cd, sbj_cd, grd_cd, trm_cd, ctg1_cd, ctg2_cd, ctg3_cd, ctg4_cd, title, desc1, cont1, smmr, crt_at, mod_at)
    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now())  
    '''

    values = (data['prptHisId'], data['genEngCd'],data['sbjCd'], data['grdCd'], data['trmCd'], data['ctg1Cd'], data['ctg2Cd'], data['ctg3Cd'],data['ctg4Cd'],data['title'],data['desc1'],data['cont1'],data['smmr'])

    cursor.execute(sql, values)
    # cursor.execute("SELECT LASTVAL()")
    data['dfnId'] = cursor.lastrowid

    sql = f'''
    insert into fingerprint_meta (prpt_his_id, dfn_id, gen_eng_cd, sbj_cd, grd_cd, trm_cd, ctg1_cd, ctg2_cd, ctg3_cd, ctg4_cd, fgpt, crt_at, mod_at)
    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now())  
    '''

    values = (data['prptHisId'], data['dfnId'], data['genEngCd'],data['sbjCd'], data['grdCd'], data['trmCd'], data['ctg1Cd'], data['ctg2Cd'], data['ctg3Cd'],data['ctg4Cd'],data['fgpt'])
    cursor.execute(sql, values)

    for qustion in data['questions']:
        sql = f'''
        insert into question_meta (prpt_his_id, dfn_id, gen_eng_cd, sbj_cd, grd_cd, trm_cd, ctg1_cd, ctg2_cd, ctg3_cd, ctg4_cd, qst, lgnds, answ, crt_at, mod_at)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now())  
        '''

        values = (data['prptHisId'], data['dfnId'], data['genEngCd'],data['sbjCd'], data['grdCd'], data['trmCd'], data['ctg1Cd'], data['ctg2Cd'], data['ctg3Cd'],data['ctg4Cd'],qustion['question'], qustion['legends'], qustion['answer'])
        cursor.execute(sql, values)
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
    
    insert_content(event, dbconn, cursor)        
    dbconn.close()
    
    return {
        "statusCode": 200,
        "body": {"message": "success"},
        "headers": {
            "Content-Type": "application/json"
        }
    }
