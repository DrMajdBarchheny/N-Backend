from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
# ---------- Category ----------


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    data = request.data
    
    # Check for required fields
    if not data.get('username'):
        return Response({'error': 'Username is required'}, status=400)
    
    if not data.get('password'):
        return Response({'error': 'Password is required'}, status=400)
    
    # Check if username already exists
    if User.objects.filter(username=data['username']).exists():
        return Response({'error': 'Username already taken'}, status=400)

    try:
        user = User.objects.create_user(
            username=data['username'],
            email=data.get('email', ''),
            password=data['password']
        )
    except Exception as e:
        return Response({'error': f'Error creating user: {str(e)}'}, status=400)

    refresh = RefreshToken.for_user(user)
    return Response({
        'user': {
            'username': user.username,
            'email': user.email,
        },
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=201)


@api_view(['GET'])

@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])

@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    data = request.data

    user.first_name = data.get('name', user.first_name)
    user.username = data.get('email', user.username)
    user.email = data.get('email', user.email)
    if data.get('password'):
        user.password = make_password(data['password'])

    user.save()

    serializer = UserSerializerWithToken(user, many=False)
    return Response(serializer.data)