
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home),
      path("products/", views.products),
        path("customer/<str:pk_test>/", views.customer),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
