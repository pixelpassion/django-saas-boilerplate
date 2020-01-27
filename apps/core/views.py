from rest_framework.response import Response
from rest_framework.views import APIView


# TODO: remove this test handler as soon as we have actual views to test against
class TestApiView(APIView):
    http_method_names = ["post"]

    def post(self, request, format=None):
        return Response({"response": "post"})
