import os
import csv
import mysql.connector
from django.contrib.auth.hashers import make_password

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings") 
import django
django.setup()

from api.models import UserSections, Modules, Sections, ModuleSections, Roles, UserProfile, StaticCountries, StaticDocumentTypes


cnx = mysql.connector.connect(user=os.environ.get('DB_USER'), password=os.environ.get('DB_PASSWORD'),
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

## read and executa store procedure

script_sql = "select * from api_userprofile;"

with open("sp/sp_get_data_user_for_email.sql", "r") as archivo:
    script_sql = archivo.read()

with cnx.cursor() as cursor:
    cursor.execute(script_sql)
    cursor.fetchall()

cnx.commit()

## 