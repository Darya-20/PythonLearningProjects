from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import *


@api_view(['POST'])
def submit_data(request):
    try:
        pass_serializer = PassSerializer(data=request.data)
        if pass_serializer.is_valid():
            pass_obj = pass_serializer.save()
            return Response({
                'status': 200,
                'message': 'Отправлено успешно',
                'id': pass_obj.id
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 400,
            'message': 'Ошибка валидации',
            'errors': pass_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'status': 500,
            'message': 'Ошибка при выполнении операции',
            'error_details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
