from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

# Create your views here.

class LoginApi(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:

            token, _ = Token.objects.get_or_create(user)

            response = {
                "message": "LoginSuccessFull",
                "token": token.key
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            response = {
                "message": "Invalid username or password"
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = User.objects.get(username='admin')
        token, _ = Token.objects.get_or_create(user=user)
        content = {
            "user": user.username,
            # "token" : user.auth_token.key
            "token": token.key
        }

        return Response(data=content, status=status.HTTP_200_OK)


@api_view(['POST'])
def logout(request):

        token = Token.objects.get(key=request.data.get('token'))
        if token is not None:
            token.delete()
            return Response(data={"message":"Sign out"}, status=status.HTTP_200_OK)
        
        return Response(data={"message":"Token Invalid"}, status=status.HTTP_400_BAD_REQUEST)
