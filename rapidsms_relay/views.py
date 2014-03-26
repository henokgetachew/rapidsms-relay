from django.shortcuts import render
from django.http import HttpResponse
from rapidsms.router import send
from rapidsms.models import Connection, Backend
from rapidsms_relay import settings

def index(request):
    phone_number = request.GET.get('phone_number','')
    message = request.GET.get('message','')
    
    conn = Connection()
    conn.identity = phone_number
    conn.backend = Backend.objects.get(name=settings.RAPIDSMS_BACKENDS_FOR_SMS_RELAY)
    
    send(message, conn)
    
    return HttpResponse("Message sent to: %s, Content: %s" % (phone_number,message))
