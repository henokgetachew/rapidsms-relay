from django.shortcuts import render
from django.http import HttpResponse
from rapidsms.router import send
from rapidsms.models import Connection, Backend
from rapidsms_relay import settings

def index(request):
    phone_number = request.GET.get('phone_number','')
    message = request.GET.get('message','')
        
    sent_identity = phone_number

    backend_to_use = Backend.objects.get(name=settings.RAPIDSMS_BACKENDS_FOR_SMS_RELAY)
    
    conn, created = Connection.objects.get_or_create(identity=sent_identity, backend = backend_to_use)
    
    send(message, conn)
    
    return HttpResponse("Message sent to: %s, Content: %s" % (phone_number,message))
