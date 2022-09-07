from django.shortcuts import render
from django.db import transaction
from django.db.models import Q, F, Func, Value, ExpressionWrapper
from django.db.models.aggregates import *
from store.models import Order, OrderItem, Product,Customer
from django.contrib.contenttypes.models import ContentType
from store.models import Product
from tags.models import TaggedItem
from django.db import connection



def say_hello(request):
# executing raw SQL queries.
# examples
# we can use also the with to get stored procedures
    # Calling a stored procedure.
    with connection.cursor() as cursor:
        cursor.callproc('get_customers', ['params'])
    return render(request, 'hello.html', {'name': 'Ambrose', 'result':list(queryset)})
