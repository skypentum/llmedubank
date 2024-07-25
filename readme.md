# LLMEdubank

LLMEdubank는 다양한 학습 문제를 자동으로 제작하고 서비스를 제공하는 Artificial Intelligence Question Generator 입니다.
각 코드별 내용은 아래 내용을 확인하시기 바랍니다.


# Backend

각 폴더별로 독립적인 코드 실행 및 컨테이너 구성을 할 수 있도록 구성하였습니다.
뿐만 아니라, AWS의 Lambda함수 구성을 할 경우에도 해당 코드 그대로 람다 함수로 구성 가능합니다.
VSCode 기준으로 환경 세팅 및 실행 방법을 가이드 합니다.

## 1. AWS Lambda Local 환경 세팅
```
공통
1. Docker Desktop 설치 (https://docs.docker.com/desktop/install/windows-install/)
2. AWS CLI 설치 (https://awscli.amazonaws.com/AWSCLIV2.msi)

Python 기준
1. Python 설치(https://www.python.org) 
2. pip 설치 (python.exe get-pip.py)
3. SAM 설치 (https://docs.aws.amazon.com/ko_kr/serverless-application-model/latest/developerguide/install-sam-cli.html)
4. window 파일 길이 강제 늘리기 : (cli : New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" ` -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force)

Visual Studio Code 
1. Visual Studio Code 설치
2. Visual Studio Code Extension 설치
  - Python
  - AWS Toolkit
  - YAML

```

## 2. AWS Lambda 개발 환경 설정
1. file 생성
```
  - events
    - event.json
{
  "first_name":"kim",
  "last_name":"Simon"    
}
```
```
  - app.py
import json

def lambda_handler(event, context):
    first_name = event['first_name']
    last_name = event['last_name']

    message = f"Hello {first_name} {last_name}!"  

    return { 
        'message' : message
    } 
```
```
  - template.yml
AWSTemplateFormatVersion : '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Resources:
  HelloNameFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: app.lambda_handler
      Runtime: python3.11
```
2. Run and Debug -> launch.json 파일 생성
```
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "type": "aws-sam",
            "request": "direct-invoke",
            "name": "serverless_311:HelloNameFunction (python3.11)",
            "invokeTarget": {
                "target": "template",
                "templatePath": "${workspaceFolder}/template.yml",
                "logicalId": "HelloNameFunction"
            },
            "lambda": {
                "payload": {
                    "path": "${workspaceFolder}/events/event.json",
                },
                "environmentVariables": {}
            }
        }
    ]
}
```

## 3. AWS Lambda Local 환경 실행
```
sma local invoke 
```
또는
Run and Debug 실행

### * 실행전 반드시 config_format.ini를 config.ini로 변경 후, 설정정보 기입 할 것.

# Frontend
---

VSCode 기준으로 실행 방법을 가이드 합니다.

## 1. 실행방법

1) VSCode의 Live Server 플러그인을 이용하여 실행
2) 웹서버 구성 후 frontend 경로를 디렉토리로 설정 
3) AWS S3 정적 웹 사이트 구성 후 해당 파일 업로드

### * 실행전 반드시 env_format.js를 env.js로 변경 후, 설정정보 기입 할 것.

# Database

## 1. DB구성

Database는 MariaDB를 사용하였으며, DDL은 database 폴더의 ddl.sql을 참고바랍니다.
Database 설계는 DB설계서를 참고바랍니다.

