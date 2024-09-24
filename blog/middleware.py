from typing import Any


class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        print(f"Request URL: {request.path} - User: {request.user} - Method: {request.method}")
        response = self.get_response(request)
        print(f"Reponse: {response}")
        
        return response