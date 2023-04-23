import os
import csv
import mysql.connector
from django.contrib.auth.hashers import make_password

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings") 
import django
django.setup()

from api.models import UserSections,PaymentMethods,Floor, Modules, Sections, ModuleSections, Roles, UserProfile, StaticCountries, StaticDocumentTypes


mydb = mysql.connector.connect(user=os.environ.get('DB_USER'), password=os.environ.get('DB_PASSWORD'),
                           host=os.environ.get('DB_HOST'),
                           database=os.environ.get('DB_NAME'))

module = ()
document = ()
user = ()

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
        user = UserProfile.objects.get_or_create(
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

        user_section = UserSections.objects.get_or_create(
            module_section = module_section[0],
            user_id = user[0].id
        )

## read and execute store procedure

archivos_sql = ['sp/1_login.sql','sp/2_get_users.sql', 'sp/3_insert_user.sql', 'sp/4_update_user.sql', 'sp/5_insert_client.sql','sp/6_update_client.sql',
                'sp/7_insert_promotion.sql','sp/8_update_promotion.sql','sp/9_insert_room_detail.sql', 'sp/10_get_clients.sql','sp/11_get_promotions.sql',
                'sp/12_update_room_detail.sql','sp/13_get_room_categories.sql','sp/14_get_reserves.sql','sp/15_insert_reserve.sql','sp/16_insert_testimonial.sql',
                'sp/17_update_testimonial.sql']
cursor = mydb.cursor()

for archivo in archivos_sql:
    with open(archivo, 'r') as f:
        contenido_sql = f.read()
        cursor.execute(contenido_sql)

mydb.close()

## 