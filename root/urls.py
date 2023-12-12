from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from root.settings import MEDIA_URL, MEDIA_ROOT, STATIC_URL, STATIC_ROOT
from root.swagger import swagger_urls, schema_view

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    # path('', include('apps.quiz.urls')),
    path('', include('apps.taxi.urls')),

] + swagger_urls + static(MEDIA_URL, document_root=MEDIA_ROOT) + static(STATIC_URL,
                                                                      document_root=STATIC_ROOT)
