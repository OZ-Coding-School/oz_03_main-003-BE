from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
# Create your views here.

class HealthCheck(GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response(
            data={
                "Message": "HELLO"
            },
            status=status.HTTP_200_OK
        )
