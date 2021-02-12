from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from wypozyczalnia.views import (
	# PrzedmiotView,
	UzytkownikView,
	WypozyczenieView,
	OpiniaView,
	DzialView,
    change_status,
    PrzedmiotyView,
    change_przedmiot,
    delete_przedmiot,
    change_uzytkownik
)
from django.contrib import admin 
from wypozyczalnia.api import RegisterAPI,LoginAPI,Logout
from knox import views as knox_views
from wypozyczalnia.api import LoginAPI
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
# router.register(r'przedmiot', PrzedmiotView)
router.register(r'uzytkownik', UzytkownikView)
router.register(r'opinie', OpiniaView)
router.register(r'wypozyczenia', WypozyczenieView)
router.register(r'dzialy', DzialView)
router.register(r'przedmiotyy',PrzedmiotyView)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('knox.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/register', RegisterAPI.as_view()),
    path('api-auth/login', LoginAPI.as_view()),
    path('api-auth/logout', Logout.as_view()),
    path('changestatus/<int:id>',change_status, name="change_status"),
    path('changeprzedmiot/<int:id>',change_przedmiot, name="change_przedmiot"),
    path('deleteprzedmiot/<int:id>',delete_przedmiot, name="delete_przedmiot"),
    path('changeuzytkownik/<int:id>',change_uzytkownik, name="change_uzytkownik"),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
