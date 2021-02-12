from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


def upload_to(instance, filename):
    return 'posts/{filename}'.format(filename=filename)


class Uzytkownik(models.Model):
    numerTelefonu = models.CharField(max_length=12)
    miasto = models.CharField(max_length=30)
    dataUrodzenia = models.DateField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.miasto  # self.user.username + " " + self.user.last_name +


class DzialPrzedmiotu(models.Model):
    nazwa = models.CharField(max_length=30)

    def __str__(self):
        return self.nazwa


class Przedmiot(models.Model):
    zdjecie = models.ImageField(
        _("Image"), upload_to="przedmiot", blank=True, null=True)
    nazwa = models.CharField(max_length=30, null=True)
    miasto = models.CharField(max_length=30, null=True)
    dzialPrzedmiotu = models.ForeignKey(
        DzialPrzedmiotu, blank=True, null=True, related_name='dzial', on_delete=models.CASCADE)
    opisPrzedmiotu = models.TextField(null=True)
    cena = models.IntegerField(blank=True, null=True)
    uzytkownikUdostepniajacy = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    dostepnoscPoczatek = models.DateField()
    dostepnoscZakonczenie = models.DateField()
    status = models.BooleanField(blank=True, null=True, default=False)

    def __str__(self):
        return str(self.status) + " " + str(self.dostepnoscPoczatek) + " " + str(self.dostepnoscZakonczenie)


class Wypozyczenie(models.Model):
    przedmiot = models.ForeignKey(Przedmiot, on_delete=models.CASCADE)
    wypozyczeniePoczatek = models.DateField()
    wypozyczenieZakonczenie = models.DateField()
    informacjeDodatkowe = models.TextField(null=True)
    uzytkownik = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.przedmiot) + " " + str(self.wypozyczeniePoczatek) + " " + str(self.wypozyczenieZakonczenie)


class Opinia(models.Model):
    opis = models.TextField(blank=True, null=True)
    skalaZadowolenia = models.IntegerField(blank=True, null=True)
    uzytkownik = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    przedmiot = models.ForeignKey(
        Przedmiot, on_delete=models.CASCADE, null=True, blank=True)
