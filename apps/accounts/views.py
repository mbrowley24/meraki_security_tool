from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator


class LoginView(APIView):
    permission_classes = [AllowAny]


    def post(self, request):

        username = request.get('username')
        password = request.get('password')

        if not username or not password:
            return Response(
                {'message': "username and password required"},
                staus = status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(request, username=username, password=password)

        if user is None:

            return Response(
                {'message': "invalid credentials"},
                status = status.HTTP_401_UNAUTHORIZED
            )
        
        login(request, user)

        return Response(
            {'message': "login successful"}
            , status = status.HTTP_200_OK
            )