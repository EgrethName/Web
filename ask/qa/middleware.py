from .models import Session
import datetime


class CheckSessionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        response = self.get_response(request)
        return response

    def process_request(self, request):
        try:
            sessionid = request.COOKIES.get('sessionid')
            session = Session.objects.get(key=sessionid, expires__gt=datetime.datetime.today(),)
            request.session = session
            request.user = session.user
        except Session.DoesNotExist:
            request.session = None
            request.user = None
