# As long as DEBUG is on:
from django.db import connection
from django.conf import settings


class SQL_Middleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        if settings.DEBUG:
            time = 0
            for query in connection.queries:
                time = time + float(query['time'])

            sql = "Number of queries:%s | Time:%s" % (len(connection.queries), time)

            response.content = response.content.decode().replace('</body>', '%s</body>' % sql).encode()
        else:
            response.content = response.content.decode().replace('</body>', 'Server is in production mode</body>').encode()

        return response
