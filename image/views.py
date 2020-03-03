from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.views import APIView
from image.models import ImageService
from image.validators import ImageCreateValidator
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile

from base64 import b64decode

from time import time
from datetime import datetime, timedelta


def get_status_transaction(get_key):
    array = {
        'Complete': 0,
        'In Progress': 1,
        'Failed': 2
    }
    return array[get_key]


class ImagenServiceViews(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        get_validation = ImageCreateValidator(request.data)

        if get_validation.validate():
            data = get_validation.data
            queryset = ImageService()

            b64_text = data['picture']
            transaction_status = get_status_transaction(data['transaction_status'])
            try:
                image_data = b64decode(b64_text)
                queryset.image = ContentFile(image_data, 'imagen.png')
            except Exception as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

            queryset.model_name = data['model']
            queryset.image_analysis = data['image_analysis_id']
            queryset.transaction_status = transaction_status
            queryset.save()

            msg = {
                "msg": "the image was created successfully",
                "data": {
                    "model": queryset.model_name,
                    "picture": queryset.image.url,
                    "image_analysis_id": queryset.image_analysis,
                    "transaction_status": queryset.get_transaction_status_display()
                }
            }

            return Response(msg, status=status.HTTP_201_CREATED)

        else:
            return Response(get_validation.errors(),
                            status=status.HTTP_400_BAD_REQUEST)
