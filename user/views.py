from django.contrib.auth import get_user_model
from rest_framework import status, permissions
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import Survivor, Advocate
from user.serializers import CustomUserSerializer, AdvocateSerializer, SurvivorSerializer

User = get_user_model()


def create_user(request):
    serializer = CustomUserSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        return serializer.save()


def update_user(user, request):
    serializer = CustomUserSerializer(user, data=request.data, partial=True)

    if serializer.is_valid(raise_exception=True):
        return serializer.save()


class SurvivorRegisterView(APIView):
    def post(self, request):
        user = create_user(request)
        survivor = Survivor.objects.create(user=user)

        return Response(SurvivorSerializer(survivor).data, status=status.HTTP_201_CREATED)


class AdvocateRegisterView(APIView):
    def post(self, request):
        user = create_user(request=request)
        advocate = Advocate.objects.create(user=user)

        return Response(AdvocateSerializer(advocate).data, status=status.HTTP_201_CREATED)


class UserIsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return view.kwargs['user_id'] == request.user.id


class UserInformationView(APIView):
    permission_classes = (
        IsAuthenticated,
        UserIsOwnerOrReadOnly,
    )

    def get(self, request, user_id):
        user = get_user(user_id)

        if hasattr(user, 'survivor'):
            survivor = Survivor.objects.get(user_id=user_id)
            result = SurvivorSerializer(survivor)
        else:
            advocate = Advocate.objects.get(user_id=user_id)
            result = AdvocateSerializer(advocate)

        return Response(result.data, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        update_user(request.user, request=request)

        user = get_user(user_id)

        if hasattr(user, 'survivor'):
            serializer = SurvivorSerializer(user.survivor, request.data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
        else:
            serializer = AdvocateSerializer(user.advocate, data=request.data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, user_id):
        user = get_user(user_id)

        user.is_active = False

        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


def get_user(user_id):
    try:
        user = User.objects.get(id=user_id)

        if user.is_active:
            return user
        else:
            raise NotFound

    except User.DoesNotExist:
        raise NotFound