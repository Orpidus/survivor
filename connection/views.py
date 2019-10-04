import time
from multiprocessing import Process

from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from connection.models import Connection
from connection.serializers import ConnectionSerializer
from notification.exponent import send_push_message
from user.models import Advocate, Survivor


class UserIsSurvivor(permissions.BasePermission):
    def has_permission(self, request, view):
        return Survivor.objects.filter(user_id=request.user.id).exists()


class RequestConnectionView(APIView):
    permission_classes = (
        IsAuthenticated,
        UserIsSurvivor,
    )

    def post(self, request):
        connection = Connection.objects.create(survivor_id=request.user.id)

        process = Process(target=request_advocates(connection_id=connection.id))
        process.start()

        return Response(connection.id, status.HTTP_200_OK)


class UserIsAdvocate(permissions.BasePermission):
    def has_permission(self, request, view):
        return Advocate.objects.filter(user_id=request.user.id).exists()


class AcceptConnectionView(APIView):
    permission_classes = (
        IsAuthenticated,
        UserIsAdvocate,
    )

    def post(self, request):
        connection = Connection.objects.get(id=request.data.get('connection_id'))

        if connection.advocate_id:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            survivor = Survivor.objects.get(user_id=connection.survivor_id)
            advocate = Advocate.objects.get(user_id=request.user.id)

            connection.advocate_id = advocate.user_id
            connection.save()

            message = f'Advocate {advocate.user.first_name} has accepted your request to connect'
            data = {
                'advocate_id': advocate.user_id
            }

            send_push_message(survivor.user.device_token, message=message, data=data)

            return Response(status=status.HTTP_200_OK)


class ListConnections(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user

        if hasattr(user, 'survivor'):
            result = Connection.objects.filter(survivor_id=user.user_token).exclude(advocate_id__isnull=True)
        else:
            result = Connection.objects.filter(advocate_id=user.id)

        return Response(ConnectionSerializer(result, many=True).data, status=status.HTTP_200_OK)


def request_advocates(connection_id):
    sleep_time = 30

    survivor_id = Connection.objects.get(id=connection_id).survivor_id
    survivor = Survivor.objects.get(user__user_token=survivor_id)

    advocates = Advocate.objects.all()

    for advocate in advocates:
        connection = Connection.objects.get(id=connection_id)

        if connection.advocate_id:
            break

        message = f'{survivor.user.first_name} has requested to connect with you'
        data = {
            'survivor_id': survivor_id,
            'connection_id': connection_id,
            **data
        }

        send_push_message(advocate.user.device_token, message=message, data=data)

        time.sleep(sleep_time)
