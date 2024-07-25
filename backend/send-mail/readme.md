# 1. AWS Lambda Local 환경 세팅
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

# 2. AWS Lambda 개발 환경 설정
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

# 3. AWS Lambda Local 환경 실행
```
sma local invoke 
```
또는
Run and Debug 실행