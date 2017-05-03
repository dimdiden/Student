from django.db import connection


class SQL_Middleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        time = 0
        for query in connection.queries:
            time = time + float(query['time'])
            
        sql = "Number of queries:%s | Time:%s" % (len(connection.queries), time)

        response.content = response.content.decode().replace('</body>', '%s</body>' % sql).encode()

        return response
