from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import RegisterView, LoginView, LogoutView

schema_view = get_schema_view(
    openapi.Info(
        title="API Docs",
        default_version='v1',
        description="Here you can find the documentation for the API of the project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="rsuarezdavid@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0),
         name="this is the API documentation"),
    path("register", RegisterView.as_view()),
    path("login", LoginView.as_view()),
    path("logout", LogoutView.as_view()),
    path("", include("CRUD_API.urls"))
]
