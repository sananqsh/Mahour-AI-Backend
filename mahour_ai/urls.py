from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include

from .swagger import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('api/llm/', include('llm_caller.urls')),
    path('api/', include('dashboard.urls')),
    path(
        'swagger/',
        login_required(schema_view.with_ui('swagger', cache_timeout=0)),
        name='schema-swagger-ui'
    ),

]
