# Generated by Django 3.1.1 on 2020-10-09 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wypozyczalnia', '0016_auto_20201009_1727'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uzytkownik',
            name='email',
        ),
        migrations.RemoveField(
            model_name='uzytkownik',
            name='haslo',
        ),
        migrations.RemoveField(
            model_name='uzytkownik',
            name='imie',
        ),
        migrations.RemoveField(
            model_name='uzytkownik',
            name='nazwisko',
        ),
    ]