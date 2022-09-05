
from django.urls import path, include
from . import views


urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
]