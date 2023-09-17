
# Create your views here.
from rest_framework import views
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from firebase_admin import auth
from .validators import validate_data
from google.cloud.firestore_v1 import Client


class CsrfExemptMixin:
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class RegisterView(CsrfExemptMixin, views.APIView):
    def post(self, request):
        data = request.data

        try:
            validate_data(data)

            name = data.get("name")
            last_name = data.get("last_name")
            email = data.get("email")
            password = data.get("password")
            phone_number = data.get("phone_number")

            user = auth.create_user(
                email=email,
                phone_number='+34' + phone_number,
                password=password,
                display_name=name + last_name)

            Client().collection(u'users').document(user.uid).set({
                u'name': name,
                u'last_name': last_name,
                u'email': email,
                u'phone_number': phone_number,
                u'uid': user.uid
            })

            return Response({"token": auth.create_custom_token(user.uid)}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class LoginView(CsrfExemptMixin, views.APIView):
    def post(self, request):
        authorization_header = request.headers.get('Bearer')
        email = request.data.get('email')
        if not authorization_header:
            return Response({"error": "Token login is missing"}, status=400)
        try:
            user = auth.get_user_by_email(email)
            response = Response({
                "login": "success",
                "user": {
                    'uid': user.uid,
                    'email': user.email,
                    'display_name': user.display_name
                }
            }, status=200)
            response.set_cookie('token', authorization_header, secure=True)
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class LogoutView(CsrfExemptMixin, views.APIView):
    def post(self, request):
        response = Response({"logout": "success"}, status=200)
        response.delete_cookie('token')
        return response
