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

from .models import Product, ProductCategory, ProductFamliy
from .serializers import ProductSerializer, ProductCategorySerializer, ProductFamilySerializer
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

class ProductFamilyApi(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        families = ProductFamliy.objects.all()
        serializer = ProductFamilySerializer(families, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = ProductFamilySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductCategoryApi(APIView):
    
    def get(self, request, format=None):
        categories = ProductCategory.objects.all()
        serializer = ProductCategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductApi(APIView):
    
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
