from rest_framework.response import Response
from rest_framework.views import APIView


class TestApiView(APIView):
    http_method_names = ["post"]

    def post(self, request, format=None):
        return Response({"response": "post"})
