from django.db import connection
from rest_framework.request import Request
from rest_framework.response import Response


class DebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: Request) -> Response:
        return self.get_response(request)

    def process_template_response(
        self, request: Request, response: Response
    ) -> Response:
        total_time = 0
        for query in connection.queries:
            total_time += float(query.get("time"))

        response["X-NS-DEBUG-TOTAL-REQUESTS"] = len(connection.queries)
        response["X-NS-DEBUG-QUERIES-TIME"] = total_time

        return response
