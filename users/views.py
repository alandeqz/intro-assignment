from cgitb import reset
from unittest import result
from django.shortcuts import render
from .models import User
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes
from django.db import connection

# Create your views here.

@api_view(['GET'])
def getBalance(request, id = 0):
    if id == 0:
        return errorResponse('received empty id')
    
    dbResult = User.objects.raw('SELECT id, balance FROM users WHERE id=\'{0}\''.format(id))

    balance = 0

    for b in dbResult:
        balance = b.balance
    
    data = {
        "balance": balance
    }

    return JsonResponse(data)

@api_view(['POST'])
@parser_classes([JSONParser])
def depositFunds(request, id = 0):
    if id == 0:
        return errorResponse('received empty id')
        
    amount = request.data['amount']

    if not isinstance(amount, int) or amount < 1:
        return errorResponse('received an invalid amount')
    
    with connection.cursor() as cursor:
        cursor.execute('UPDATE users SET balance=balance+{0} WHERE id={1}'.format(amount, id))

    return okResponse()

@api_view(['POST'])
@parser_classes([JSONParser])
def chargeFunds(request, id = 0):
    if id == 0:
        return errorResponse('received empty id')
        
    amount = request.data['amount']

    if not isinstance(amount, int) or amount < 1:
        return errorResponse('received an invalid amount')
    
    with connection.cursor() as cursor:
        cursor.execute('UPDATE users SET balance=CASE WHEN balance - {0} > 0 THEN balance - {0} ELSE 0 END WHERE id={1}'.format(amount, id))

    return okResponse()

def errorResponse(message):
    data = {
        "error": "{0}".format(message)
    }

    return JsonResponse(data)

def okResponse():
    result = {
        "status": "OK"
    }

    return JsonResponse(result)
