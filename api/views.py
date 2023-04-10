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
import json
from .utils import executeSP
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

            result = executeSP('get_data_user_for_email',[email])[0]
            if result["arr_modules"] and  result["arr_sections"]:
                result["arr_modules"] = json.loads(result["arr_modules"])
                result["arr_sections"] = json.loads(result["arr_sections"])
                result["ability"] = {"action": "manage", "subject": "all"}

            response = {
                "message": "LoginSuccessFull",
                "token": token.key,
                "user":result
            }

            return Response(data=response, status=status.HTTP_200_OK)

        except UserProfile.DoesNotExist:
            return Response(data={"message": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        email = request.data.get('email')
        user = UserProfile.objects.get(email=email)
        token, _ = Token.objects.get_or_create(user=user)
        content = {
            "user": user.email,
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

@api_view(['POST'])
def viewGetUsers(request):
    search_txt = request.data.get('search_txt')
    perpage = request.data.get('perpage') if request.data.get('perpage') else 10
    npage = request.data.get('npage') if request.data.get('npage') else 1
    orderBy = request.data.get('orderBy') if request.data.get('orderBy') else 'desc'
    date_from = request.data.get('date_from') # 2022-10-1 format YYYY-MM-DD
    date_to = request.data.get('date_to')
    is_active = request.data.get('status') if request.data.get('status') else None
    country = request.data.get('country_id') if request.data.get('country_id') else None
    document_type = request.data.get('document_type_id') if request.data.get('document_type_id') else None
    role_id = request.data.get('role_id') if request.data.get('role_id') else None
    parameters = [
        search_txt,
        perpage,
        npage,
        orderBy,
        date_from,
        date_to,
        is_active,
        country,
        document_type,
        role_id]
    result = executeSP('get_users',parameters)
    content = {
        "data":result,
    }
    return Response(data=content, status=status.HTTP_200_OK)