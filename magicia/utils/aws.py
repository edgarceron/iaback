import boto3
from io import BytesIO
from iaback.settings import AWS_STORAGE_BUCKET_NAME, AWS_S3_ACCESS_KEY_ID, AWS_S3_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME

def create_label_resource_file(results: list, file_name: str):
    s3 = boto3.resource('s3')
    session = s3.Bucket(AWS_STORAGE_BUCKET_NAME)
    output = BytesIO()
    for i in results:
        output.write(bytes(i + '\n', 'utf-8'))
    output.seek(0)
    session.put_object(
        Key=file_name,
        Body=output
    )


def run_download_task(file_name: str) -> dict:
    ecs = boto3.client('ecs', region_name='us-east-1')
    response = ecs.run_task(
        cluster='iaback',
        taskDefinition='iabackimages',
        launchType='FARGATE',
        networkConfiguration= { 
            "awsvpcConfiguration": {
                "subnets": [ "subnet-0a4e12d90255c296a" ],
                "securityGroups": ['sg-043ba56f0fafb4b3f'],
                "assignPublicIp": "ENABLED"
            }
        },
        overrides= {
            'containerOverrides': [{
                'name': 'iabackimages',
                'environment': [
                    {
                        'name': 'LABEL_FILE',
                        'value': file_name
                    },
                    {
                        'name': 'AWS_ACCESS_KEY_ID',
                        'value': AWS_S3_ACCESS_KEY_ID
                    },
                    {
                        'name': 'AWS_SECRET_ACCESS_KEY',
                        'value': AWS_S3_SECRET_ACCESS_KEY
                    },
                    {
                        'name': 'AWS_BUCKET_NAME',
                        'value': AWS_STORAGE_BUCKET_NAME
                    }
                ]
            }]
        }
    )
    return response
