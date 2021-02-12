from rest_framework import mixins
from rest_framework import viewsets
from . models import Przedmiot, Uzytkownik, Wypozyczenie, Opinia, DzialPrzedmiotu
from . serializers import UzytkownikSerializer, WypozyczenieSerializer, OpiniaSerializer, DzialSerializer, PrzedmiotySerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view
import datetime


class PrzedmiotyView(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Przedmiot.objects.all()
    serializer_class = PrzedmiotySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['miasto', 'nazwa',
                        'dzialPrzedmiotu', 'uzytkownikUdostepniajacy']


@api_view(['PATCH'])
def change_status(request, id):
    if request.method == 'PATCH':
        przedmiot = Przedmiot.objects.get(id=id)
        przedmiot.status = not przedmiot.status
        przedmiot.save()
        return Response(f'Przedmiot {przedmiot.nazwa} zmienil status na {przedmiot.status}')


@api_view(['PUT'])
def change_przedmiot(request, id):
    if request.method == 'PUT':
        przedmiot = Przedmiot.objects.get(id=id)
        print("\n\n\n put \n\n\n ", request.data, " \n\n\n")
        przedmiot.nazwa = request.data.get(
            "nazwa") if request.data.get("nazwa") else przedmiot.nazwa
        przedmiot.miasto = request.data.get(
            "miasto") if request.data.get("miasto") else przedmiot.miasto
        przedmiot.opisPrzedmiotu = request.data.get("opisPrzedmiotu") if request.data.get(
            "opisPrzedmiotu") else przedmiot.opisPrzedmiotu
        przedmiot.dostepnoscPoczatek = przedmiot.dostepnoscPoczatek if request.data.get(
            "dostepnoscPoczatek") == datetime.date(1000, 10, 10) else request.data.get("dostepnoscPoczatek")
        przedmiot.dostepnoscZakonczenie = przedmiot.dostepnoscZakonczenie if request.data.get(
            "dostepnoscZakonczenie") == datetime.date(1000, 10, 16) else request.data.get("dostepnoscZakonczenie")
        przedmiot.save()
        return Response(f'xd')


@api_view(['DELETE'])
def delete_przedmiot(request, id):
    if request.method == 'DELETE':
        przedmiot = Przedmiot.objects.get(id=id)
        przedmiot.delete()
        return Response(f'deletehehe')

# def date(self):
#         cleaned_data = super().clean()
#         dataPoczatek = cleaned_data.get("start_date")
#         dataZakonczenie = cleaned_data.get("end_date")
#         if dataPoczatek < dataZakonczenie:
#             raise ValidationError("Koncowa data nie moze byc wieksza od poczatkowej" % (self.dataPoczatek, self.dataZakonczenie))


class UzytkownikView(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Uzytkownik.objects.all()
    serializer_class = UzytkownikSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']


@api_view(['PUT'])
def change_uzytkownik(request, id):
    if request.method == 'PUT':
        uzytkownik = Uzytkownik.objects.get(id=id)
        print("\n\n\n put \n\n\n ", request.data, " \n\n\n")
        uzytkownik.user.username = request.data.get("username") if request.data.get(
            "username") else uzytkownik.user.username
        uzytkownik.user.first_name = request.data.get("first_name") if request.data.get(
            "first_name") else uzytkownik.user.first_name
        uzytkownik.user.last_name = request.data.get("last_name") if request.data.get(
            "last_name") else uzytkownik.user.last_name
        uzytkownik.user.email = request.data.get(
            "email") if request.data.get("email") else uzytkownik.user.email
        uzytkownik.numerTelefonu = request.data.get("numerTelefonu") if request.data.get(
            "numerTelefonu") else uzytkownik.numerTelefonu
        uzytkownik.miasto = request.data.get(
            "miasto") if request.data.get("miasto") else uzytkownik.miasto
        uzytkownik.dataUrodzenia = request.data.get("dataUrodzenia") if request.data.get(
            "dataUrodzenia") else uzytkownik.dataUrodzenia
        uzytkownik.save()
        uzytkownik.user.save()
        return Response(f'xd')


class WypozyczenieView(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    queryset = Wypozyczenie.objects.all()
    serializer_class = WypozyczenieSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['uzytkownik']


class OpiniaView(mixins.CreateModelMixin,
                 mixins.DestroyModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Opinia.objects.all()
    serializer_class = OpiniaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['przedmiot']


class DzialView(mixins.CreateModelMixin,
                mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):
    queryset = DzialPrzedmiotu.objects.all()
    serializer_class = DzialSerializer
