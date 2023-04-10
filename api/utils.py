from django.db import connection


def executeSP(sp, parametres):
    cursor = connection.cursor()
    cursor.callproc(sp,parametres)
    columns = [column[0] for column in cursor.description]
    results = cursor.fetchall()
    objects = []
    for row in results:
        obj = {}
        for i, column in enumerate(columns):
            obj[column] = row[i]
        objects.append(obj)
    cursor.close()
    return objects