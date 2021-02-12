from django.contrib import admin
from .models import Przedmiot
from .models import Uzytkownik
from .models import Wypozyczenie

# Register your models here.
admin.site.register(Przedmiot)
admin.site.register(Uzytkownik)
admin.site.register(Wypozyczenie)