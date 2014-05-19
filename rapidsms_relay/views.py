import urllib
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import RequestContext
from django.utils.html import escape
from rapidsms.router import send
from rapidsms.models import Connection, Backend
from rapidsms_relay import settings


def choose_backend(phone_no):
    try:
        matching_dict = settings.RAPIDSMS_BACKENDS_COUNTRY_CODE_MATCHING_FOR_SMS_RELAY
    except:
        raise ImproperlyConfigured

    backend = None
    for key in matching_dict.keys():
        if phone_no.startswith(key):
            backend = matching_dict[key]
    if backend is None:
        backend = matching_dict['default']
    return Backend.objects.get(name=backend)


def index(request):
    phone_number = request.GET.get('phone_number', '')
    message = request.GET.get('message', '')

    sent_identity = phone_number

    backend_to_use = choose_backend(phone_number)

    conn, created = Connection.objects.get_or_create(identity=sent_identity, backend=backend_to_use)

    send(message, conn)

    return HttpResponse("Message sent to: %s, Content: %s" % (phone_number, message))


@login_required
def send_outgoing(request):
    """
    Used for the purposes of showing a testing page
    :param request:
    :return: HTTPResponse
    """
    if request.method == 'POST':
        phone_number = request.POST.get("phone_number")
        message = escape(request.POST.get("msg"))
        params = dict(phone_number=phone_number, message=message)
        params = urllib.urlencode(params)
        url = '{0:s}?{1:s}'.format(settings.RAPIDSMS_HOST_RELAY_URL, params)
        urllib.urlopen(url).read()

    template = get_template('rapidsms_relay_tester.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))


