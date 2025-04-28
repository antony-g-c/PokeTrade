"""
URL configuration for PokeTrade project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('marketplace1/', include(('marketplace1.urls', 'marketplace1'), namespace='marketplace1')),
    path('trade/', include(('trade.urls', 'trade'), namespace='trade')),
    path('orders/', include(('orders.urls', 'orders'), namespace='orders')),
    path('', include(('collection.urls', 'collection'), namespace='collection')),
    path('login/', include(('login.urls', 'login'), namespace='login')),
    path('accounts/', include('django.contrib.auth.urls')),
]