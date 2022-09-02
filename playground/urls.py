from importlib.resources import path
from django.urls import path, include
from . import views


urlpatterns = [
    path(''),
    path('__debug__/', include('debug_toolbar.urls')),
]