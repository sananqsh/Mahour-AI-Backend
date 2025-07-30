from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Mahour AI API",
        default_version='v1',
        description="API Specifications",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="sananqsh@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny,],
)
