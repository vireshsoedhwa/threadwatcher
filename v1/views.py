from django.shortcuts import render
from rest_framework import generics

from rest_framework.views import APIView
from rest_framework.response import Response

import logging
logger = logging.getLogger(__name__)

from .tasks import get_all_threads, filter_threads

# Create your views here.
class GetB(APIView):

    def get(self, request, format=None):              

        # x = requests.get('https://a.4cdn.org/b/catalog.json')

        # logger.error(x.json())

        # for page in x.json():   
        #     for thread in page['threads']: 
        #         print(thread['no'])
                # logger.error(thread['com'])
                # newthread = bThread.objects.create(id=thread['no'], summary=thread['com'])
                # newthread.save()

        # logger.error(x.json()[0]['page'])


        get_all_threads()
        filter_threads()

        return Response('x.json()')