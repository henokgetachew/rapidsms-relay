from rapidsms.apps.base import AppBase
from rapidsms_relay import settings
from atom.http_core import HttpResponse
import urllib

class RelayApp(AppBase):
    
    def relayToUrl(self, message, phone_no):
        url = "%s?message=%s&phone_no=%s" % (settings.INCOMING_MESSAGES_RELAY_URL,message.replace(' ','%20'), phone_no)
        urllib.urlopen(url).read()        

    
    def handle(self,msg):
        if (msg.text.startswith(settings.INCOMING_MESSAGES_RELAY_INDICATOR_SMS_PREFIX) or settings.INCOMING_MESSAGES_RELAY_EVERYTHING):
            self.relayToUrl(msg.text,msg.connection.identity)
            msg.respond('The server has received your message.')
            return True
        return False
    