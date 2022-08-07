from magicia.utils.aws import create_label_resource_file, run_download_task
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from fastbook import search_images_bing
from iaback.settings import AZURE_SEARCH_KEY
# Create your views here.


@api_view(['POST'])
def search_images(request):
    labels = request.data.get('labes', [])
    tasks = []
    for o in labels:
        #create an S3 file. The label will be the name of the file
        #insert the bing urls into the file
        #launch an ECS tasks
        results = search_images_bing(AZURE_SEARCH_KEY, f'{o}', max_images=5).attrgot('contentUrl')
        create_label_resource_file(results, o)
        response = run_download_task(o)
        tasks.append(response["taskArn"])
    
    return Response(
        {
            'tasks': tasks 
        },
        status=status.HTTP_200_OK,
        content_type='application/json'
    )

        


        
