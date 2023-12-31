# Create your views here.
from rest_framework import views
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from firebase_admin import auth
from firebase_admin import firestore
from .validators import validate_data


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

            firestore.client().collection(u'users').document(user.uid).set({
                u'name': name,
                u'last_name': last_name,
                u'email': email,
                u'phone_number': phone_number,
                u'uid': user.uid,
                u'password': password,
            })

            return Response({"token": auth.create_custom_token(user.uid)}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class LoginView(CsrfExemptMixin, views.APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = auth.get_user_by_email(email)
            response = Response({
                "login": "success",
                "user": {
                    'uid': user.uid,
                    'email': user.email,
                    'display_name': user.display_name,
                    "token": auth.create_custom_token(user.uid)
                }
            }, status=200)
            doc_snap = firestore.client().collection(u'users').document(user.uid).get()
            if (doc_snap.get('password') != request.data.get('password')):
                return Response({"error": "Contraseña incorrecta"}, status=400)
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=400)
