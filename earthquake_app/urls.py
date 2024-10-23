"""
URL configuration for earthquake_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from earthquakes.views import EarthquakeSearchView, EarthquakeResultView
from earthquakes.views import CityViewSet, HomePageView

router = DefaultRouter()
router.register(r'cities', CityViewSet)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/cities/<int:city_id>/earthquakes/',
         EarthquakeSearchView.as_view(), name='search-earthquake'),
    path('api/cities/results/<str:task_id>',
         EarthquakeResultView.as_view(), name='earthquake-results'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
