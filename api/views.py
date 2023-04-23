from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import UserProfile, Roles, StaticDocumentTypes, StaticCountries, RoomCategory, Floor, Promotion
from django.contrib.auth.hashers import check_password, make_password

import json
from .utils import executeSP, paginateBootrstapVue
from .serializers import RoleSerializer, DocumentTypeSerializer, CountrySerializer, CategorySerializer, FloorSerializer, PromotionSerializer
from django.utils.text import slugify


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


def generate_slug(name):
    return slugify(name)

@api_view(['GET'])
def viewGetRoles(request):
    roles = Roles.objects.all()
    serializer = RoleSerializer(roles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def viewGetDocumentTypes(request):
    document_types = StaticDocumentTypes.objects.all()
    serializer = DocumentTypeSerializer(document_types, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def viewGetCountries(request):
    countries = StaticCountries.objects.all()
    serializer = CountrySerializer(countries, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def viewGetCategoriesList(request):
    categories = RoomCategory.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def viewGetRoomFloorsList(request):
    floors = Floor.objects.all()
    serializer = FloorSerializer(floors, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def viewGetRoomPromotionsList(request):
    promotions = Promotion.objects.all()
    serializer = PromotionSerializer(promotions, many=True)
    return Response(serializer.data)


# User
@api_view(['POST'])
def viewRegisterUser(request):

    password =  request.data.get('password')
    document_number = request.data.get('document_number')
    phone = request.data.get('phone')

    user = {
        "first_name":  request.data.get('first_name'),
        "last_name": request.data.get('last_name'),
        "email": request.data.get('email'),
        "password_user": make_password(password) if password else make_password(document_number),
        "phone": phone if phone else '',
        "country": request.data.get('country'),
        "document_type": request.data.get('document_type'),
        "document_number": request.data.get('document_number'),
        "personal_type": request.data.get('personal_type'),
        "role": request.data.get('role')
    }

    parameters = [
        json.dumps(user)
    ]
    result = executeSP('insert_user',parameters)
    return Response(data=json.loads(result[0]["response"]), status=status.HTTP_200_OK)

@api_view(['POST'])
def viewUpdateUser(request):

    phone = request.data.get('phone')

    user = {
        "id": request.data.get('id'),
        "email": request.data.get('email'),
        "phone": phone if phone else '',
        "country": request.data.get('country'),
        "personal_type": request.data.get('personal_type'),
        "role": request.data.get('role'),
        "status": request.data.get('is_active')
    }

    parameters = [
        json.dumps(user)
    ]
    result = executeSP('update_user',parameters)
    return Response(data=json.loads(result[0]["response"]), status=status.HTTP_200_OK)

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
    
    return Response(data=paginateBootrstapVue(result=result,page=npage,perpage=perpage), status=status.HTTP_200_OK)

# Promotion
@api_view(['POST'])
def viewRegisterPromotion(request):
        promotion = {
            "name":  request.data.get('name'),
            "cost": request.data.get('cost'),
            "image": request.data.get('image'),
            "description": request.data.get('description'),
            "status": 1,
        }
        parameters = [
            json.dumps(promotion)
        ]
        result = executeSP('insert_promotion',parameters)
        return Response(data=json.loads(result[0]["response"]), status=status.HTTP_200_OK)


@api_view(['POST'])
def viewGetPromotions(request):
    search_txt = request.data.get('search_txt')
    perpage = request.data.get('perpage') if request.data.get('perpage') else 10
    npage = request.data.get('npage') if request.data.get('npage') else 1
    orderBy = request.data.get('orderBy') if request.data.get('orderBy') else 'desc'
    date_from = request.data.get('date_from') # 2022-10-1 format YYYY-MM-DD
    date_to = request.data.get('date_to')
    status_promotion = request.data.get('status') if request.data.get('status') else None
    parameters = [
        search_txt,
        perpage,
        npage,
        orderBy,
        date_from,
        date_to,
        status_promotion,
    ]
    result = executeSP('get_promotions',parameters)
    
    return Response(data=paginateBootrstapVue(result=result,page=npage,perpage=perpage), status=status.HTTP_200_OK)

# Category
@api_view(['POST'])
def viewRegisterCategory(request):
        category = {
            "name":  request.data.get('name'),
            "slug": slugify(request.data.get('name')),
            "color": request.data.get('color'),
            "description": request.data.get('description'),
            "image": request.data.get('image'),
            "status": 1,
        }
        parameters = [
            json.dumps(category)
        ]
        result = executeSP('insert_category',parameters)
        return Response(data=json.loads(result[0]["response"]), status=status.HTTP_200_OK)

@api_view(['POST'])
def viewUpdateCategory(request):

    category = {
        "id": request.data.get('id'),
        "name": request.data.get('name'),
        "slug": slugify(request.data.get('name')),
        "color": request.data.get('color'),
        "description": request.data.get('description'),
        "image": request.data.get('image'),
        "status": request.data.get('status')
    }

    parameters = [
        json.dumps(category)
    ]
    result = executeSP('update_category',parameters)
    return Response(data=json.loads(result[0]["response"]), status=status.HTTP_200_OK)

@api_view(['POST'])
def viewGetCategories(request):
    search_txt = request.data.get('search_txt')
    perpage = request.data.get('perpage') if request.data.get('perpage') else 10
    npage = request.data.get('npage') if request.data.get('npage') else 1
    orderBy = request.data.get('orderBy') if request.data.get('orderBy') else 'desc'
    date_from = request.data.get('date_from') # 2022-10-1 format YYYY-MM-DD
    date_to = request.data.get('date_to')
    parameters = [
        search_txt,
        perpage,
        npage,
        orderBy,
        date_from,
        date_to,
    ]
    result = executeSP('get_room_categories2',parameters)
    
    return Response(data=paginateBootrstapVue(result=result,page=npage,perpage=perpage), status=status.HTTP_200_OK)

# Banner
@api_view(['POST'])
def viewRegisterBanner(request):
        banner = {
            "image":  request.data.get('image'),
            "status": 1,
        }
        parameters = [
            json.dumps(banner)
        ]
        result = executeSP('insert_banner',parameters)
        return Response(data=json.loads(result[0]["response"]), status=status.HTTP_200_OK)

@api_view(['POST'])
def viewUpdateBanner(request):

    banner = {
        "id": request.data.get('id'),
        "image": request.data.get('image'),
        "status": request.data.get('status')
    }

    parameters = [
        json.dumps(banner)
    ]
    result = executeSP('update_banner',parameters)
    return Response(data=json.loads(result[0]["response"]), status=status.HTTP_200_OK)

@api_view(['POST'])
def viewGetBanners(request):
    search_txt = request.data.get('search_txt')
    perpage = request.data.get('perpage') if request.data.get('perpage') else 10
    npage = request.data.get('npage') if request.data.get('npage') else 1
    orderBy = request.data.get('orderBy') if request.data.get('orderBy') else 'desc'
    date_from = request.data.get('date_from') # 2022-10-1 format YYYY-MM-DD
    date_to = request.data.get('date_to')
    parameters = [
        search_txt,
        perpage,
        npage,
        orderBy,
        date_from,
        date_to,
    ]
    result = executeSP('get_banners',parameters)
    
    return Response(data=paginateBootrstapVue(result=result,page=npage,perpage=perpage), status=status.HTTP_200_OK)

# Client
@api_view(['POST'])
def viewRegisterClient(request):
    client = {
        "first_name":  request.data.get('first_name'),
        "last_name": request.data.get('last_name'),
        "email": request.data.get('email'),
        "phone": request.data.get('phone'),
        "country": request.data.get('country'),
        "document_type": request.data.get('document_type'),
        "document_number": request.data.get('document_number'),
        "status": request.data.get('status'),
    }
    parameters = [
        json.dumps(client)
    ]
    result = executeSP('insert_client',parameters)
    return Response(data=json.loads(result[0]["response"]), status=status.HTTP_200_OK)

@api_view(['POST'])
def viewUpdateClient(request):

    phone = request.data.get('phone')

    client = {
        "id": request.data.get('id'),
        "email": request.data.get('email'),
        "first_name":  request.data.get('first_name'),
        "last_name":  request.data.get('last_name'),
        "phone": phone if phone else '',
        "country": request.data.get('country'),
        "document_type": request.data.get('document_type'),
        "document_number": request.data.get('document_number'),
        "status": request.data.get('status')
    }

    parameters = [
        json.dumps(client)
    ]
    result = executeSP('update_client',parameters)
    return Response(data=json.loads(result[0]["response"]), status=status.HTTP_200_OK)

@api_view(['GET'])
def viewGetClientsSelect(request):
    parameters = []
    result = executeSP('get_clients_select',parameters)
    return Response(data=result, status=status.HTTP_200_OK)

@api_view(['POST'])
def viewGetClients(request):
    search_txt = request.data.get('search_txt')
    perpage = request.data.get('perpage') if request.data.get('perpage') else 10
    npage = request.data.get('npage') if request.data.get('npage') else 1
    orderBy = request.data.get('orderBy') if request.data.get('orderBy') else 'desc'
    date_from = request.data.get('date_from') # 2022-10-1 format YYYY-MM-DD
    date_to = request.data.get('date_to')
    status_client = request.data.get('status') if request.data.get('status') else None
    country = request.data.get('country_id') if request.data.get('country_id') else None
    document_type = request.data.get('document_type_id') if request.data.get('document_type_id') else None
    parameters = [
        search_txt,
        perpage,
        npage,
        orderBy,
        date_from,
        date_to,
        document_type,
        status_client,
        country]
    result = executeSP('get_clients',parameters)
    
    return Response(data=paginateBootrstapVue(result=result,page=npage,perpage=perpage), status=status.HTTP_200_OK)

# Promotions
@api_view(['POST'])
def viewRegisterPromotion(request):

    promotion = {
        "name":  request.data.get('name'),
        "cost": request.data.get('cost'),
        "description": request.data.get('description'),
        "image": request.data.get('image'),
        "status": 1,
    }

    parameters = [
        json.dumps(promotion)
    ]
    result = executeSP('insert_promotion',parameters)
    return Response(data=json.loads(result[0]["response"]), status=status.HTTP_200_OK)

@api_view(['POST'])
def viewUpdatePromotion(request):

    promotion = {
        "id": request.data.get('id'),
        "name":  request.data.get('name'),
        "cost": request.data.get('cost'),
        "description": request.data.get('description'),
        "image": request.data.get('image'),
        "status": request.data.get('status'),
    }

    parameters = [
        json.dumps(promotion)
    ]
    result = executeSP('update_promotion',parameters)
    return Response(data=json.loads(result[0]["response"]), status=status.HTTP_200_OK)

@api_view(['POST'])
def viewGetPromotions(request):
    search_txt = request.data.get('search_txt')
    perpage = request.data.get('perpage') if request.data.get('perpage') else 10
    npage = request.data.get('npage') if request.data.get('npage') else 1
    orderBy = request.data.get('orderBy') if request.data.get('orderBy') else 'desc'
    date_from = request.data.get('date_from') # 2022-10-1 format YYYY-MM-DD
    date_to = request.data.get('date_to')
    status_promotion = request.data.get('status') if request.data.get('status') else None
    parameters = [
        search_txt,
        perpage,
        npage,
        orderBy,
        date_from,
        date_to,
        status_promotion]
    result = executeSP('get_promotions',parameters)
    
    return Response(data=paginateBootrstapVue(result=result,page=npage,perpage=perpage), status=status.HTTP_200_OK)

# Reserve
@api_view(['POST'])
def viewRegisterReserve(request):
    
    detail = request.data.get('detail')
    reserve = {
        "client":  request.data.get('client'),
        "personal":  request.data.get('personal'),
        "payment_method": request.data.get('payment_method'),
        "description": request.data.get('description'),
        "total": request.data.get('total'),
         "observation": "ninguna",
        "reserve_date": "2023-10-1",
    }

    print(detail)
    parameters = [
        json.dumps(reserve),
        json.dumps(detail)
    ]
    result = executeSP('insert_reserve',parameters)
    return Response(data=json.loads(result[0]["response"]), status=status.HTTP_200_OK)

@api_view(['POST'])
def viewUpdateReserve(request):

    reserve = {
        "id": request.data.get('id'),
        "client":  request.data.get('client'),
        "personal":  request.data.get('personal'),
        "payment_method": request.data.get('payment_method'),
        "description": request.data.get('description'),
        "total": request.data.get('total'),
        "detail": request.data.get('detail'),
        "status": request.data.get('status')
    }

    parameters = [
        json.dumps(reserve)
    ]
    result = executeSP('update_reserve',parameters)
    return Response(data=json.loads(result[0]["response"]), status=status.HTTP_200_OK)

@api_view(['POST'])
def viewGetReserves(request):
    search_txt = request.data.get('search_txt')
    perpage = request.data.get('perpage') if request.data.get('perpage') else 10
    npage = request.data.get('npage') if request.data.get('npage') else 1
    orderBy = request.data.get('orderBy') if request.data.get('orderBy') else 'desc'
    date_from = request.data.get('date_from') # 2022-10-1 format YYYY-MM-DD
    date_to = request.data.get('date_to')
    status_room = request.data.get('status') if request.data.get('status') else None
    client = request.data.get('client') if request.data.get('client') else None
    room = request.data.get('room') if request.data.get('room') else None
    parameters = [
        search_txt,
        perpage,
        npage,
        orderBy,
        date_from,
        date_to,
        # room
        # status,
        # client,
    ]
    result = executeSP('get_reserves',parameters)
    
    return Response(data=paginateBootrstapVue(result=result,page=npage,perpage=perpage), status=status.HTTP_200_OK)


# Room
@api_view(['POST'])
def viewRegisterRoom(request):

    room = {
        "name": request.data.get('name'),
        "slug": slugify(request.data.get('name')),
        "guest_number": request.data.get('guest_number'),
        "number": request.data.get('number'),
        "description": request.data.get('description'),
        "has_bed": request.data.get('has_bed') if request.data.get('has_bed') else 0,
        "has_wifi": request.data.get('has_wifi') if request.data.get('has_wifi') else 0,
        "has_balcony": request.data.get('has_balcony') if request.data.get('has_balcony') else 0,
        "has_tv": request.data.get('has_tv') if request.data.get('has_tv') else 0,
        "has_hot_water": request.data.get('has_hot_water') if request.data.get('has_hot_water') else 0,
        "has_jacuzzi": request.data.get('has_jacuzzi') if request.data.get('has_jacuzzi') else 0,
        "has_private_bathroom": request.data.get('has_private_bathroom') if request.data.get('has_private_bathroom') else 0,
        "has_couch": request.data.get('has_couch') if request.data.get('has_couch') else 0,
        "floor":  request.data.get('floor_id'),
        "promotion": request.data.get('promotion_id'),
        "category": request.data.get('category_id'),
        "cost": request.data.get('cost'),
        "status": 1,
    }

    parameters = [
        json.dumps(room)
    ]
    result = executeSP('insert_room',parameters)
    return Response(data=json.loads(result[0]["response"]), status=status.HTTP_200_OK)

@api_view(['POST'])
def viewUpdateRoom(request):

    room = {
        "id": request.data.get('id'),
        "name": request.data.get('name'),
        "description": request.data.get('description'),
        "guest_number": request.data.get('guest_number'),
        "number": request.data.get('number'),
        "has_bed": request.data.get('has_bed'),
        "has_tv": request.data.get('has_tv'),
        "has_hot_water": request.data.get('has_hot_water'),
        "has_jacuzzi": request.data.get('has_jacuzzi'),
        "has_private_bathroom": request.data.get('has_private_bathroom'),
        "has_couch": request.data.get('has_couch'),
        "has_balcony": request.data.get('has_balcony'),
        "has_wifi": request.data.get('has_wifi'),
        "cost": request.data.get('cost'),
        "status": request.data.get('status'),
        "category_id": request.data.get('category_id'),
        "slug": request.data.get('slug'),
        "floor_id": request.data.get('floor_id'),
        "promotion_id": request.data.get('promotion_id'),
    }

    parameters = [
        json.dumps(room)
    ]
    result = executeSP('update_room',parameters)
    return Response(data=json.loads(result[0]["response"]), status=status.HTTP_200_OK)

@api_view(['GET'])
def viewGetRoomsSelect(request):
    
    parameters = []
    result = executeSP('get_rooms_select',parameters)
    return Response(data=result, status=status.HTTP_200_OK)

@api_view(['GET'])
def viewGetMethodSelect(request):
    
    parameters = []
    result = executeSP('get_method_select',parameters)
    return Response(data=result, status=status.HTTP_200_OK)

@api_view(['POST'])
def viewGetRooms(request):
    search_txt = request.data.get('search_txt')
    perpage = request.data.get('perpage') if request.data.get('perpage') else 10
    npage = request.data.get('npage') if request.data.get('npage') else 1
    orderBy = request.data.get('orderBy') if request.data.get('orderBy') else 'desc'
    date_from = request.data.get('date_from') # 2022-10-1 format YYYY-MM-DD
    date_to = request.data.get('date_to')
    status_room = request.data.get('status') if request.data.get('status') else None
    floor=  request.data.get('floor'),
    personal=  request.data.get('personal'),
    promotion= request.data.get('promotion'),
    category= request.data.get('category'),
    guest_number= request.data.get('guest_number'),
    number= request.data.get('number'),
    has_bed= request.data.get('has_bed'),
    has_tv= request.data.get('has_tv'),
    has_hot_water= request.data.get('has_hot_water'),
    has_jacuzzi= request.data.get('has_jacuzzi'),
    has_private_bathroom= request.data.get('has_private_bathroom'),
    has_couch= request.data.get('has_couch'),
    has_wifi= request.data.get('has_wifi'),
    parameters = [
        search_txt,
        perpage,
        npage,
        orderBy,
        date_from,
        date_to,
        # status,
        # floor,
        # personal,
        # promotion,
        # category,
        # guest_number,
        # number,
        # has_bed,
        # has_tv,
        # has_hot_water,
        # has_jacuzzi,
        # has_private_bathroom,
        # has_couch,
        # has_wifi,
    ]
    result = executeSP('get_rooms',parameters)
    
    return Response(data=paginateBootrstapVue(result=result,page=npage,perpage=perpage), status=status.HTTP_200_OK)


# Testimonial
@api_view(['POST'])
def viewRegisterTestimonial(request):

    testimonial = {
        "description": request.data.get('description'),
        "client": request.data.get('client'),
        "reserve": request.data.get('reserve'),
        "room": request.data.get('room'),
        "status": 1,
    }

    parameters = [
        json.dumps(testimonial)
    ]
    result = executeSP('insert_testimonial',parameters)
    return Response(data=json.loads(result[0]["response"]), status=status.HTTP_200_OK)

@api_view(['POST'])
def viewUpdateTestimonial(request):

    testimonial = {
        "id": request.data.get('id'),
        "description": request.data.get('description'),
        "client": request.data.get('client'),
        "reserve": request.data.get('reserve'),
        "room": request.data.get('room'),
       "status": request.data.get('status')
    }

    parameters = [
        json.dumps(testimonial)
    ]
    result = executeSP('update_testimonial',parameters)
    return Response(data=json.loads(result[0]["response"]), status=status.HTTP_200_OK)

@api_view(['POST'])
def viewGetTestimonials(request):
    search_txt = request.data.get('search_txt')
    perpage = request.data.get('perpage') if request.data.get('perpage') else 10
    npage = request.data.get('npage') if request.data.get('npage') else 1
    orderBy = request.data.get('orderBy') if request.data.get('orderBy') else 'desc'
    date_from = request.data.get('date_from') # 2022-10-1 format YYYY-MM-DD
    date_to = request.data.get('date_to')
    client = request.data.get('client')
    parameters = [
        search_txt,
        perpage,
        npage,
        orderBy,
        date_from,
        date_to
    ]
    result = executeSP('get_testimonials',parameters)
    
    return Response(data=paginateBootrstapVue(result=result,page=npage,perpage=perpage), status=status.HTTP_200_OK)


@api_view(['GET'])
def viewGetDashboardIndicators(request):
    result = executeSP('get_dashboard_data',[])
    return Response(data=result, status=status.HTTP_200_OK)


@api_view(['POST'])
def viewGetCalendarReserves(request):
    start_date = request.data.get('start_date')
    end_date = request.data.get('end_date')
    parameters = [
        start_date,
        end_date,
    ]
    result = executeSP('get_calendar_reserves',parameters)
    return Response(data=result, status=status.HTTP_200_OK)