#!/usr/bin/env python3
import json
from pathlib import Path


root = Path(__file__).resolve().parents[1]
lambda_code = (root / "lambda" / "progress_app.py").read_text(encoding="utf-8")

template = {
    "AWSTemplateFormatVersion": "2010-09-09",
    "Description": "JDU teacher progress server: HTTPS API, short-lived dashboard sessions, and email-linked server progress",
    "Parameters": {
        "LambdaExecutionRoleName": {
            "Type": "String",
            "Default": "LabRole",
            "AllowedPattern": "[A-Za-z0-9+=,.@_-]+",
            "Description": "Existing AWS Academy role used by Lambda",
        },
        "AdminKeyHash": {
            "Type": "String",
            "NoEcho": True,
            "AllowedPattern": "[0-9a-f]{64}",
        },
        "RegistrationKeyHash": {
            "Type": "String",
            "NoEcho": True,
            "AllowedPattern": "[0-9a-f]{64}",
        },
        "SessionTtlSeconds": {
            "Type": "Number",
            "Default": 1800,
            "MinValue": 300,
            "MaxValue": 3600,
        },
    },
    "Resources": {
        "ProgressTable": {
            "Type": "AWS::DynamoDB::Table",
            "Properties": {
                "BillingMode": "PAY_PER_REQUEST",
                "AttributeDefinitions": [{"AttributeName": "pk", "AttributeType": "S"}],
                "KeySchema": [{"AttributeName": "pk", "KeyType": "HASH"}],
                "SSESpecification": {"SSEEnabled": True},
                "TimeToLiveSpecification": {"AttributeName": "expiresAt", "Enabled": True},
                "Tags": [
                    {"Key": "JDUCourse", "Value": "Introduction_CyberSecurity"},
                    {"Key": "JDUManagedBy", "Value": "CloudFormation"},
                ],
            },
        },
        "ProgressFunction": {
            "Type": "AWS::Lambda::Function",
            "Properties": {
                "Runtime": "python3.12",
                "Handler": "index.handler",
                "Role": {"Fn::Sub": "arn:${AWS::Partition}:iam::${AWS::AccountId}:role/${LambdaExecutionRoleName}"},
                "MemorySize": 256,
                "Timeout": 15,
                "Environment": {
                    "Variables": {
                        "TABLE_NAME": {"Ref": "ProgressTable"},
                        "ADMIN_KEY_HASH": {"Ref": "AdminKeyHash"},
                        "REGISTRATION_KEY_HASH": {"Ref": "RegistrationKeyHash"},
                        "SESSION_TTL_SECONDS": {"Ref": "SessionTtlSeconds"},
                    }
                },
                "Code": {"ZipFile": lambda_code},
                "Tags": [
                    {"Key": "JDUCourse", "Value": "Introduction_CyberSecurity"},
                    {"Key": "JDUManagedBy", "Value": "CloudFormation"},
                ],
            },
        },
        "ProgressApi": {
            "Type": "AWS::ApiGatewayV2::Api",
            "Properties": {"Name": {"Fn::Sub": "${AWS::StackName}-api"}, "ProtocolType": "HTTP"},
        },
        "ProgressIntegration": {
            "Type": "AWS::ApiGatewayV2::Integration",
            "Properties": {
                "ApiId": {"Ref": "ProgressApi"},
                "IntegrationType": "AWS_PROXY",
                "IntegrationUri": {"Fn::GetAtt": ["ProgressFunction", "Arn"]},
                "PayloadFormatVersion": "2.0",
                "TimeoutInMillis": 15000,
            },
        },
        "DefaultStage": {
            "Type": "AWS::ApiGatewayV2::Stage",
            "Properties": {
                "ApiId": {"Ref": "ProgressApi"},
                "StageName": "$default",
                "AutoDeploy": True,
                "DefaultRouteSettings": {"ThrottlingBurstLimit": 50, "ThrottlingRateLimit": 20},
            },
        },
        "InvokePermission": {
            "Type": "AWS::Lambda::Permission",
            "Properties": {
                "Action": "lambda:InvokeFunction",
                "FunctionName": {"Ref": "ProgressFunction"},
                "Principal": "apigateway.amazonaws.com",
                "SourceArn": {"Fn::Sub": "arn:${AWS::Partition}:execute-api:${AWS::Region}:${AWS::AccountId}:${ProgressApi}/*"},
            },
        },
    },
    "Outputs": {
        "BaseUrl": {
            "Description": "HTTPS endpoint used by students and the teacher helper",
            "Value": {"Fn::Sub": "https://${ProgressApi}.execute-api.${AWS::Region}.${AWS::URLSuffix}"},
        },
        "ProgressTableName": {"Value": {"Ref": "ProgressTable"}},
        "DashboardCommand": {"Value": "jdu-dashboard"},
    },
}

for logical_id, method, path in [
    ("RegisterRoute", "POST", "/register"),
    ("StatusRoute", "POST", "/status"),
    ("EmailRoute", "POST", "/link-email"),
    ("SubmitRoute", "POST", "/submit"),
    ("SessionRoute", "POST", "/admin/session"),
    ("DashboardRoute", "GET", "/dashboard"),
    ("StudentSessionRoute", "POST", "/student/session"),
    ("StudentProgressRoute", "GET", "/student/progress"),
    ("HealthRoute", "GET", "/health"),
]:
    template["Resources"][logical_id] = {
        "Type": "AWS::ApiGatewayV2::Route",
        "Properties": {
            "ApiId": {"Ref": "ProgressApi"},
            "RouteKey": f"{method} {path}",
            "Target": {"Fn::Join": ["/", ["integrations", {"Ref": "ProgressIntegration"}]]},
        },
    }

destination = root / "cloudformation" / "progress-server.json"
destination.parent.mkdir(parents=True, exist_ok=True)
destination.write_text(json.dumps(template, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print(destination)
