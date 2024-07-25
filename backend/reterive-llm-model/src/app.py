import json
import time
import pymysql
import boto3
import os
import configparser

# from poe_api_wrapper import PoeApi
# from langchain_community.llms import Bedrock
# from langchain_aws import BedrockLLM

ENV_TYPE = os.getenv('envType', 'LOCAL')
config_file = "config.ini"

config = configparser.ConfigParser()
config.read(config_file)

session = boto3.Session(
    aws_access_key_id=config.get(ENV_TYPE, 'AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=config.get(ENV_TYPE, 'AWS_SECRET_ACCESS_KEY'),
    region_name= config.get(ENV_TYPE, 'REGION_NAME')
)

def call_llm_aws_boto3(event, dbconn):
    model = event['model']
    prompt = event['prompt']
    if event['useDefaultJsonFormat']:
        prompt += '''응답은 json 포멧으로 다음과 같이 응답해줘.
            description: 개념 내용
            summary: 개념 내용 요약(50자 이내)
            fingerprint: 지문 내용
            questions: 배열 형태의 문제, 보기, 답
            - qustion: 문제 내용
            - legends: 문자열 형태의 보기
            - answer: 답
        '''

    bedrock = session.client(service_name='bedrock-runtime') #creates a Bedrock client
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
        "temperature": 0.5,
        "top_p": 0.9
    })

    response = bedrock.invoke_model(body=body, modelId=model, accept='application/json', contentType='application/json') #send the payload to Bedrock

    response_body = json.loads(response.get('body').read()) # read the response
    response_text = response_body.get("content")[0].get("text") #extract the text from the JSON response    
    print(response_text)

    return {
        'model': model,
        'prompt': prompt,
        'response_text': response_text
    }
    

def insert_prompt_history(result_data, dbconn, cursor):
    prpt_his_id = int(time.time())
    
    sql = '''
    insert into prompt_history (prpt_his_id, gen_eng_cd, prpt, result, crt_at) 
    values (%s, %s, %s, %s, now())  
    '''

    data = (prpt_his_id, result_data['model'],result_data['prompt'], result_data['response_text'])

    cursor.execute(sql, data)
    dbconn.commit()


def select_prompt_history(cursor):
    sql = "SELECT prpt_his_id, gen_eng_cd, prpt, result FROM prompt_history order by prpt_his_id desc limit 1;"
    cursor.execute(sql)
    tmp_result = cursor.fetchall()

    result = {
        "prpt_his_id": tmp_result[0]['prpt_his_id'],
        "gen_eng_cd": tmp_result[0]['gen_eng_cd'],
        "prpt": tmp_result[0]['prpt'],
        "result": json.loads(tmp_result[0]['result'], strict=False)
    }
    
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

    result_data = call_llm_aws_boto3(event, dbconn)
    insert_prompt_history(result_data, dbconn, cursor)
    response_data = select_prompt_history(cursor)
    dbconn.close()
    
    return  {
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": response_data,
        "headers": {
            "Content-Type": "application/json"
        }
    }