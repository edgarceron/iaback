import boto3
from io import StringIO

def create_label_resource_file(results: list, file_name: str):
    s3 = boto3.resource('s3')
        
    output = StringIO()
    for i in results:
        output.write(i)
    
    s3.put_object(
        Key=file_name,
        Body=output
    )


def run_download_task(file_name: str) -> dict:
    ecs = boto3.resource('ecs')
    response = ecs.run_task(
        taskDefinition='iabackimages',
        capacityProviderStrategy=[
            {
                "capacityProvider": "FARGATE_SPOT",
                "weight": 1
            }
        ],
        launchType='FARGATE',
        overrides= {
            'containerOverrides': [{
                'environment': [
                    {
                        'name': 'LABEL_FILE',
                        'value': file_name
                    },
                ]
            }]
        }
    )
    return response
