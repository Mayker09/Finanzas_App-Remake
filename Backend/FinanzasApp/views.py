from rest_framework.decorators import api_view
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def register(request):
    serializers = UserSerializer(data=request.data)
    if serializers.is_valid:
        serializers.save()
        user = User.create.get(username=serializers.data['username'])
        user.set_password(serializers.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token':token.key, "user":serializers.data }, status=status.HTTP_201_CREATED)
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username = request.data['username'])
    if not user.check_password(request.data['password']):
        return Response ({"error": "invalid password"}, status=status.HTTP_400_BAD_REQUEST)

    token, created = Token.objects.get_or_create(user=user)
    serializers = UserSerializer (instance=user)

    return Response ({"token": token.key, "user": serializers.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    return Response("estas logeado como: {}".format (request.user.username), status=status.HTTP_200_OK)
