from django.db import connection
import math
import calendar


def executeSP(sp, parametres):
    cursor = connection.cursor()
    cursor.callproc(sp, parametres)
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


def paginateBootrstapVue(result, perpage, page):

    total = result[0]["cc"] if len(result) else len(result)
    from_to = ((page - 1) * perpage) + 1
    next_page = page + 1
    last_page = max(int(math.ceil(float(total) / perpage)), 1)
    prev_page = page - 1
    perpage = perpage
    to = (page * perpage)
    paginate = {
        "current_page": page,
        "data": result,
        "first_page_url": "/?page=1",
        "from": from_to,
        "last_page": last_page,
        "last_page_url": "/?page=" + str(last_page),
        "next_page_url": "/?page=" + str(next_page) if page != last_page else "",
        "path": "/",
        "per_page": perpage,
        "prev_page_url": "/?page=" + str(prev_page) if page != 1 else "",
        "perpage": perpage,
        "to": to,
        "total": total
    }

    return paginate


def getNumberOfMonth(month):
    names_of_months = [
        "Enero",
        "Febrero",
        "Marzo",
        "Abril",
        "Mayo",
        "Junio",
        "Julio",
        "Agosto",
        "Septiembre",
        "Octubre",
        "Noviembre",
        "Diciembre",
    ]
    return (names_of_months.index(month) + 1)
