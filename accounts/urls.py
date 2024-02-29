
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),
      path("products/", views.products, name='products'),
        path("customer/<str:pk_test>/", views.customer, name='customer'),
        path('create_order/', views.createOrder, name='create_order'),
        path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
