from cgitb import reset
import json
from re import I
import re
from unittest import result
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes
from django.db import connection
from orders.serializers import OrderSerializer
from users.models import User
from .models import Order
from django.core import serializers

# Create your views here.
@api_view(['POST'])
@parser_classes([JSONParser])
def createOrder(request):
    if not isinstance(request.data['price'], int) or request.data['price'] == 0:
        return errorResponse('received an invalid price', 400)

    if not isinstance(request.data['user_id'], int) or request.data['user_id'] == 0:
        return errorResponse('received an invalid user', 400)
    
    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO orders (price, is_active, "user") VALUES ({0}, false, {1})'.format(request.data['price'], request.data['user_id']))
    
    return okResponse()

@api_view(['GET'])
@parser_classes([JSONParser])
def getOrderByID(request, id = 0):
    if id == 0:
        return errorResponse('received empty id', 400)
    
    dbResult = Order.objects.raw('SELECT * FROM orders WHERE id = {0}'.format(id))

    data = {}

    for o in dbResult:
        data['id'] = o.id
        data['price'] = o.price
        data['is_active'] = o.is_active

        userDBResult = User.objects.raw('SELECT * FROM users WHERE id = {0}'.format(o.user))

        for u in userDBResult:
            data['user'] = {}
            data['user']['id'] = u.id
            data['user']['first_name'] = u.first_name
            data['user']['last_name'] = u.last_name
            data['user']['balance'] = u.balance

    return JsonResponse(data)

@api_view(['GET'])
@parser_classes([JSONParser])
def getOrders(request):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')

    if limit == None:
        limit = 100
    
    if offset == None:
        offset = 0

    dbResult = Order.objects.raw('SELECT * FROM orders ORDER BY id LIMIT {0} OFFSET {1}'.format(limit, offset))
    
    result = []

    for o in dbResult:
        data = {}

        data['id'] = o.id
        data['price'] = o.price
        data['is_active'] = o.is_active

        userDBResult = User.objects.raw('SELECT * FROM users WHERE id = {0}'.format(o.user))

        for u in userDBResult:
            data['user'] = {}
            data['user']['id'] = u.id
            data['user']['first_name'] = u.first_name
            data['user']['last_name'] = u.last_name
            data['user']['balance'] = u.balance
        
        result.append(data)
    
    return JsonResponse(result, safe=False)


@api_view(['POST'])
@parser_classes([JSONParser])
def payOrder(request):
    orderID = request.data['order_id']

    if not isinstance(orderID, int) or orderID == 0:
        return errorResponse('received an invalid amount', 400)

    orderDBResult = Order.objects.raw('SELECT * FROM orders WHERE id = {0}'.format(orderID))

    userID = 0

    price = 0

    for o in orderDBResult:
        price = o.price

        userDBResult = User.objects.raw('SELECT id FROM users WHERE id = {0}'.format(o.user))

        for u in userDBResult:
            userID = u.id
    
    user = User.objects.raw('SELECT * FROM users WHERE id = {0}'.format(userID))

    for u in user:
        if u.balance < price:
            return errorResponse('insufficient balance amount', 403)

    with connection.cursor() as cursor:
        cursor.execute('UPDATE users SET balance = balance - {0} WHERE id = {1}'.format(price, userID))
    
    with connection.cursor() as cursor:
        cursor.execute('UPDATE orders SET is_active = true')
    
    return okResponse()

@api_view(['POST'])
@parser_classes([JSONParser])
def refundOrder(request, id = 0):
    if id == 0:
        return errorResponse('received empty id', 400)
    
    orderDBResult = Order.objects.raw('SELECT * FROM orders WHERE id = {0}'.format(id))

    userID = 0

    price = 0

    for o in orderDBResult:
        price = o.price

        userDBResult = User.objects.raw('SELECT id FROM users WHERE id = {0}'.format(o.user))

        for u in userDBResult:
            userID = u.id

    with connection.cursor() as cursor:
        cursor.execute('UPDATE users SET balance = balance + {0} WHERE id = {1}'.format(price, userID))

    with connection.cursor() as cursor:
        cursor.execute('UPDATE orders SET is_active = false')
    
    return okResponse()


@api_view(['GET'])
@parser_classes([JSONParser])
def getUserOrders(request, id = 0):
    if id == 0:
        return errorResponse('received empty id', 400)
    
    orderDBResult = Order.objects.raw('SELECT * FROM orders WHERE "user" = {0}'.format(id))

    result = []

    userInfo = {}

    userDBResult = User.objects.raw('SELECT * FROM users WHERE id = {0}'.format(id))

    for u in userDBResult:
        userInfo['id'] = u.id
        userInfo['first_name'] = u.first_name
        userInfo['last_name'] = u.last_name
        userInfo['balance'] = u.balance

    for o in orderDBResult:
        data = {}

        data['id'] = o.id
        data['price'] = o.price
        data['is_active'] = o.is_active
        data['user'] = userInfo
        
        result.append(data)
    
    return JsonResponse(result, safe=False)


def errorResponse(message, statusCode=500):
    data = {
        "error": "{0}".format(message)
    }

    return JsonResponse(data, status=statusCode)

def okResponse():
    result = {
        "status": "OK"
    }

    return JsonResponse(result)
