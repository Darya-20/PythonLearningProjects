from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import *


@extend_schema(
    summary="Отправка данных о перевале",
    description="Создаёт запись о перевале с данными пользователя, координат, уровня сложности и изображений.",
    request=PassSerializer,
    responses={
        201: OpenApiResponse(description="Запись создана"),
        400: OpenApiResponse(description="Ошибка валидации"),
        500: OpenApiResponse(description="Внутренняя ошибка",)
    },
)
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

@extend_schema(
    summary="Получение полной информации о перевале",
    description="Возвращает полную информацию о перевале по его идентификатору.",
    responses=PassSerializer
)
@api_view(['GET'])
def pass_detail(request, pk):
    try:
        pass_obj = Pass.objects.get(id=pk)
        serializer = PassSerializer(pass_obj)
        return Response(serializer.data)
    except Pass.DoesNotExist:
        return Response({'error': 'Запись не найдена'}, status=status.HTTP_404_NOT_FOUND)
    
@extend_schema(
    summary="Редактирование данных перевала",
    description="Редактирует существующую запись, если она в статусе new. Запрещено изменять любые данные пользователя.",
    request=PassSerializer,
    responses={
        200: OpenApiResponse(description="Запись успешно обновлена"),
        400: OpenApiResponse(description="Ошибка валидации или попытка изменить данные пользователя"),
        403: OpenApiResponse(description="Редактирование запрещено (неверный статус)"),
        404: OpenApiResponse(description="Запись не найдена"),
    }
)
@api_view(['PATCH'])
def update_pass(request, pk):
    try:
        pass_obj = Pass.objects.get(id=pk)

        if pass_obj.status != 'new':
            return Response({
                'state': 0,
                'message': f'Редактирование запрещено: запись имеет статус "{pass_obj.status}". Разрешено только для статуса "new".'
            }, status=status.HTTP_403_FORBIDDEN)
        
        if 'user' in request.data:
            return Response({
                'state': 0,
                'message': 'Запрещено изменять данные пользователя (ФИО, email, телефон)'
            }, status=status.HTTP_400_BAD_REQUEST)

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


@extend_schema(
    summary="Получение списка перевалов",
    description="Возвращает список данных обо всех объектах, которые пользователь с почтой <email> отправил на сервер.",
    request=PassSerializer,
    responses={
        200: OpenApiResponse(description="Список успешно получен"),
        400: OpenApiResponse(description="Отсутствует обязательный параметр user__email"),
        404: OpenApiResponse(description="Пользователь не существует"),
        500: OpenApiResponse(description="Ошибка при выполнении операции"),
    }
)
@api_view(['GET'])
def list_by_user_email(request):
    email = request.query_params.get('user__email')
    if not email:
        return Response({
            'status': 400,
            'message': 'Параметр user__email обязателен'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_exists = User.objects.filter(email=email).exists()
        if not user_exists:
            return Response({
                'status': 404,
                'message': f'Пользователь с email {email} не найден'
            }, status=status.HTTP_404_NOT_FOUND)

        passes = Pass.objects.filter(user__email=email)
        serializer = PassSerializer(passes, many=True)
        return Response({
            'status': 200,
            'count': passes.count(),
            'results': serializer.data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 500,
            'message': 'Ошибка при выполнении операции',
            'error_details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
