from django.http import JsonResponse
import os


class GatewayTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.expected_token = os.getenv("GATEWAY_SERVICE_TOKEN")

    def __call__(self, request):
        if request.path.startswith("/admin"):
            return self.get_response(request)

        token = request.headers.get("X-Gateway-Token")

        if not token:
            return JsonResponse({"error": "Token requerido"}, status=401)

        if token != self.expected_token:
            return JsonResponse({"error": "Token inválido"}, status=403)

        return self.get_response(request)
    