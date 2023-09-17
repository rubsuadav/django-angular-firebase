
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

            db = firestore.client()

            db.collection(u'users').document(user.uid).set({
                u'name': name,
                u'last_name': last_name,
                u'email': email,
                u'phone_number': phone_number,
                u'uid': user.uid
            })

            return Response({"token": auth.create_custom_token(user.uid)}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
