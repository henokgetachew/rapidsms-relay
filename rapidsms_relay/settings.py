
#Settings for elmis-relay
RAPIDSMS_BACKENDS_FOR_SMS_RELAY = "elmis_tropo_backend"
INCOMING_MESSAGES_RELAY_EVERYTHING = "True"
#If the relay everything is false, then define a prefix
INCOMING_MESSAGES_RELAY_INDICATOR_SMS_PREFIX = "elmis"
INCOMING_MESSAGES_RELAY_URL = "http://localhost:9091/sms"