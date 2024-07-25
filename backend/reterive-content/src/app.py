import os
import pymysql
import configparser

ENV_TYPE = os.getenv('envType', 'LOCAL')
config_file = "config.ini"

config = configparser.ConfigParser()
config.read(config_file)


def select_content_detail(condition, cursor):
    sql = f'''SELECT dm.dfn_id as dfnId,
        dm.prpt_his_id as prptHisId,
        dm.gen_eng_cd as genEngCd,
        dm.sbj_cd as sjbCd, 
        dm.grd_cd as grdCd, 
        dm.ctg1_cd as ctg1Cd,
        dm.ctg2_cd as ctg2Cd,
        dm.title,
        dm.desc1 as description,
        fm.fgpt_id as fgptId,
        fm.fgpt as fingerprint
        FROM define_meta dm
        inner join fingerprint_meta fm 
        on dm.dfn_id = fm.dfn_id
        where 1=1
    '''
    whereStr = ""
    if condition['dfnId']:
        whereStr += f" and dm.dfn_id = {condition['dfnId']}"
    
    sql += whereStr
    print(sql)
    cursor.execute(sql)
    dfnInfo = cursor.fetchall()

    sql = f'''SELECT 
        qm.qst_id as qstId,
        qm.qst as question,
        qm.lgnds as legends,
        qm.answ as answer
        FROM question_meta qm     
        where 1=1
    '''
    whereStr = ""
    if condition['dfnId']:
        whereStr += f" and qm.dfn_id = {condition['dfnId']}"
    
    sql += whereStr
    print(sql)
    cursor.execute(sql)
    questions = cursor.fetchall()

    result = {
        "dfnInfo": dfnInfo[0],
        "description": dfnInfo[0]['description'],
        "fingerprint": dfnInfo[0]['fingerprint'],
        "questions": questions
    }
        
    return result


def select_contents(condition, cursor):
    sql = f'''select dfn_id,
        prpt_his_id,
        gen_eng_cd,
        sbj_cd, 
        grd_cd, 
        trm_cd,
        ctg1_cd,
        ctg2_cd,
        title,
        DATE_FORMAT(crt_at, '%Y-%m-%d %H:%i:%s') AS crt_at,
        DATE_FORMAT(mod_at, '%Y-%m-%d %H:%i:%s') AS mod_at 
        from define_meta dm
        where 1=1
    '''
    
    whereStr = ""    
    if condition['genEngCd']:
        whereStr += f" and gen_eng_cd = '{condition['genEngCd']}'"
    if condition['sbjCd']:
        whereStr += f" and sbj_cd = '{condition['sbjCd']}'"
    if condition['grdCd']:
        whereStr += f" and grd_cd = '{condition['grdCd']}'"
    if condition['trmCd']:
        whereStr += f" and trm_cd = '{condition['trmCd']}'"
    if condition['ctg1Cd']:
        whereStr += f" and ctg1_cd = '{condition['ctg1Cd']}'"
    
    sql += whereStr
    sql += f" limit {condition['pageSize']} offset {condition['startPage']}"
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchall()
    
    return result


def lambda_handler(event, context):  
    dbconn = pymysql.connect(
        user=config.get(ENV_TYPE, 'DBUSER'), 
        passwd=config.get(ENV_TYPE, 'DBPASSWD'), 
        host=config.get(ENV_TYPE, 'DBHOST'), 
        db=config.get(ENV_TYPE, 'DBNAME'), 
        charset=config.get(ENV_TYPE, 'DBCHARSET')
    )
    cursor = dbconn.cursor(pymysql.cursors.DictCursor)
 
    if event['type'] == 'list':
        response_data = select_contents(event, cursor)    
    else :
        response_data = select_content_detail(event, cursor)    
    
    dbconn.close()

    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": response_data,
        "headers": {
            "Content-Type": "application/json"
        }
    }
