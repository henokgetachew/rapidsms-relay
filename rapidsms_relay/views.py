from django.shortcuts import render
from django.http import HttpResponse
from rapidsms.router import send
from rapidsms.models import Connection, Backend
from rapidsms_relay import settings

def choose_backend (phone_no):
    matching_dict = settings.RAPIDSMS_BACKENDS_COUNTRY_CODE_MATCHING_FOR_SMS_RELAY
    backend = None
    for key in matching_dict.keys():
        if (phone_no.startswith(key)):
            backend = matching_dict[key]
    backend = matching_dict['default']
    return Backend.objects.get(name = backend)      
        

def index(request):
    phone_number = request.GET.get('phone_number','')
    message = request.GET.get('message','')
        
    sent_identity = phone_number

    backend_to_use = choose_backend(phone_number)
    
    conn, created = Connection.objects.get_or_create(identity=sent_identity, backend = backend_to_use)
    
    send(message, conn)
    
    return HttpResponse("Message sent to: %s, Content: %s" % (phone_number,message))
