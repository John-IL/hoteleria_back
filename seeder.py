import os
import csv
import mysql.connector
from django.contrib.auth.hashers import make_password
from api.utils import executeSP
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings") 
import django
django.setup()

from api.models import UserSections,PaymentMethods,Floor, Modules, Sections, ModuleSections, Roles, UserProfile, StaticCountries, StaticDocumentTypes


mydb = mysql.connector.connect(user=os.environ.get('DB_USER'), password=os.environ.get('DB_PASSWORD'),
                           host=os.environ.get('DB_HOST'),
                           database=os.environ.get('DB_NAME'))

module = ()
document = ()
user = []

with open('data/modules.csv', newline='', encoding='utf-8-sig', mode='r') as f:
    reader = csv.reader(f, delimiter=';')
    for row in reader:
        created = Modules.objects.get_or_create(
            name=row[1],
            route=row[2],
            initial=row[3],
            icons=row[4],
        )

        module = created[0]

with open('data/roles.csv', newline='', encoding='utf-8-sig', mode='r') as f:
    reader = csv.reader(f, delimiter=';')
    for row in reader:
        created = Roles.objects.get_or_create(
            name=row[1],
            slug=row[2],
            description=row[3]
        )


with open('data/countries.csv', newline='', encoding='utf-8-sig', mode='r') as f:
    reader = csv.reader(f, delimiter=';')
    for row in reader:
        created = StaticCountries.objects.get_or_create(
            name=row[0],
            iso=row[1]
        )

with open('data/floor.csv', newline='', encoding='utf-8-sig', mode='r') as f:
    reader = csv.reader(f, delimiter=';')
    for row in reader:
        created = Floor.objects.get_or_create(
             number=row[0],
        )

with open('data/method.csv', newline='', encoding='utf-8-sig', mode='r') as f:
    reader = csv.reader(f, delimiter=';')
    for row in reader:
        created = PaymentMethods.objects.get_or_create(
            name=row[0]
        )

with open('data/documents.csv', newline='', encoding='utf-8-sig', mode='r') as f:
    reader = csv.reader(f, delimiter=';')
    for row in reader:
        created = StaticDocumentTypes.objects.get_or_create(
            name=row[0],
            sunat_code=row[1]
        )
        document = created

with open('data/user.csv', newline='', encoding='utf-8-sig', mode='r') as f:
    reader = csv.reader(f, delimiter=';')
    for row in reader:
        user_aux = UserProfile.objects.get_or_create(
            first_name=row[1],
            last_name=row[2],
            country_id=row[3],
            phone=row[4],
            email=row[5],
            document_type=document[0],
            document_number=row[7],
            role_id=row[8],
            personal_type=1,
            password=make_password(password=row[9])
        )

        user.append(user_aux[0])

with open('data/sections.csv', newline='', encoding='utf-8-sig', mode='r') as f:
    reader = csv.reader(f, delimiter=';')
    for row in reader:
        section = Sections.objects.get_or_create(
            name=row[1],
            route=row[2],
            is_new=row[3],
            icon=row[4],
            status=row[5]
        )
        module_section = ModuleSections.objects.get_or_create(
            section_id=section[0].id,
            module_id=module.id
        )

        for item in user:
            user_section = UserSections.objects.get_or_create(
                module_section = module_section[0],
                user_id = item.id
            )


path_migrations = 'sp/' 
archivos_sql = os.listdir('sp')
cursor = mydb.cursor()

for archivo in archivos_sql:
    with open(path_migrations+archivo, 'r') as f:
        contenido_sql = f.read()
        cursor.execute(contenido_sql)

with open('data/clients.csv', newline='', encoding='utf-8-sig', mode='r') as f:
    reader = csv.reader(f, delimiter=';')
    for row in reader:
        client = {
        "first_name":  row[0],
        "last_name": row[1],
        "email": row[3],
        "phone": row[2],
        "country": 1,
        "document_type": 1,
        "document_number": row[4],
        "status": 1,
        }
        parameters = [
            json.dumps(client)
        ]
        result = executeSP('insert_client', parameters)

with open('data/room_category.csv', newline='', encoding='utf-8-sig', mode='r') as f:
    reader = csv.reader(f, delimiter=';')
    for row in reader:
        category = {
            "name":  row[0],
            "slug": row[1],
            "color": row[2],
            "description": row[4] ,
            "status": 1,
        }
        parameters = [
            json.dumps(category)
        ]
        result = executeSP('insert_category', parameters)

    promotion = {
        "name":  "Basica",
        "cost": 0,
        "description": "Es la promocion por defecto",
        "status": 1,
    }

    parameters = [
        json.dumps(promotion)
    ]
    result = executeSP('insert_promotion', parameters)

with open('data/rooms.csv', newline='', encoding='utf-8-sig', mode='r') as f:
    reader = csv.reader(f, delimiter=';')
    for row in reader:
        room = {
        "name": row[1],
        "slug": row[2],
        "guest_number": row[3],
        "number": row[4],
        "description": row[5],
        "has_bed": row[6],
        "has_tv": row[7],
        "has_hot_water": row[8],
        "has_jacuzzi": row[9],
        "has_private_bathroom": row[10],
        "has_couch": row[11],
        "has_balcony": row[12],
        "has_wifi": row[13],
        "cost": row[14],
        "status": 1,
        "category": row[17],
        "floor":  row[18],
        "promotion": row[19]
        }
        parameters = [
            json.dumps(room)
        ]
        result = executeSP('insert_room', parameters)


mydb.close()

