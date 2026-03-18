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


@api_view(['GET'])
def pass_detail(request, pk):
    try:
        pass_obj = Pass.objects.get(id=pk)
        serializer = PassSerializer(pass_obj)
        return Response(serializer.data)
    except Pass.DoesNotExist:
        return Response({'error': 'Запись не найдена'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['PATCH'])
def update_pass(request, pk):
    try:
        pass_obj = Pass.objects.get(id=pk)

        if pass_obj.status != 'new':
            return Response({
                'state': 0,
                'message': f'Редактирование запрещено: запись имеет статус "{pass_obj.status}". Разрешено только для статуса "new".'
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = PassSerializer(pass_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'state': 1,
                'message': 'Обновлено успешно'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'state': 0,
                'message': 'Ошибка валидации',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    except Pass.DoesNotExist:
        return Response({
            'state': 0,
            'message': 'Запись не найдена'
        }, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def list_by_user_email(request):
    email = request.query_params.get('user__email')
    if not email:
        return Response({
            'status': 400,
            'message': 'Параметр user__email обязателен'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        passes = Pass.objects.filter(user__email=email)
        serializer = PassSerializer(passes, many=True)
        return Response({
            'status': 200,
            'count': passes.count(),
            'results': serializer.data
        })
    except Exception as e:
        return Response({
            'status': 500,
            'message': 'Ошибка при выполнении операции',
            'error_details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
