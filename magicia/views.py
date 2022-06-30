from django.shortcuts import render
from rest_framework.decorators import api_view
from fastbook import search_images_bing
# Create your views here.


@api_view(['POST'])
def search_images(request):
    labels = request.data.get('labes', [])
    for o in labels:
        #create an S3 resource
        #create a folder on the S3 resource
        #save the images in the S3 resource
        dest = (path/o)
        dest.mkdir(exist_ok=True)
        results = search_images_bing(key, f'{o} bear')
        download_images(dest, urls=results.attrgot('contentUrl'))

