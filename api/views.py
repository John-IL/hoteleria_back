from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import UserProfile
from django.contrib.auth.hashers import check_password
from django.db import connection
import json
# Create your views here.

class LoginApi(APIView):

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = UserProfile.objects.get(email=email)

            if user is None:
                return Response(data={"message": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

            if not user.is_active:
                return Response(data={"message": "Is not authorized"}, status=status.HTTP_400_BAD_REQUEST)

            pwd_valid = check_password(password, user.password)

            if not pwd_valid:
                return Response(data={"message": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
            
            token, _ = Token.objects.get_or_create(user=user)

            cursor = connection.cursor()

            cursor.callproc('get_data_user_for_email', [email])
            result_sp = cursor.fetchall()[0]
            module = json.loads(result_sp[9])
            sections = json.loads(result_sp[10])

            response = {
                        "message": "LoginSuccessFull",
                        "token": token.key,
                        "data": [result_sp[:9],module,sections]
                        }

            cursor.close()
            return Response(data=response, status=status.HTTP_200_OK)
        
        except UserProfile.DoesNotExist:
            return Response(data={"message": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

        

    def get(self, request):
        username = request.data.get('username')
        user = User.objects.get(username=username)
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
        return Response(data={"message": "Sign out"}, status=status.HTTP_200_OK)

    return Response(data={"message": "Token Invalid"}, status=status.HTTP_400_BAD_REQUEST)
