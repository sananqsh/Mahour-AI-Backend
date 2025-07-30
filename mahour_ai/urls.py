from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include

from .swagger import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include([
        path('accounts/', include('accounts.urls')),
        path('llm/', include('llm_caller.urls')),
        path('dashboard/', include('dashboard.urls')),
    ])),
    path(
        'swagger/',
        login_required(schema_view.with_ui('swagger', cache_timeout=0)),
        name='schema-swagger-ui'
    ),

]
