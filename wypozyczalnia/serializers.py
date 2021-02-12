from rest_framework import serializers
from wypozyczalnia.models import Przedmiot, Wypozyczenie, Opinia, Uzytkownik, DzialPrzedmiotu
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class UzytkownikSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Uzytkownik
        fields = '__all__'

    def create(self, validated_data):
        ordered_dict = validated_data['user']
        new_user = User()
        new_user.username = ordered_dict['username']
        new_user.first_name = ordered_dict['first_name']
        new_user.last_name = ordered_dict['last_name']
        new_user.email = ordered_dict['email']
        validated_data['user'] = new_user
        new_user.save()
        print("validated_data: ", validated_data)
        print("*****\n\n\n*************\n\n\n\n")
        uzytkownik = Uzytkownik.objects.create(**validated_data)
        return uzytkownik


class DzialSerializer(serializers.ModelSerializer):
    class Meta:
        model = DzialPrzedmiotu
        fields = '__all__'


class PrzedmiotySerializer(serializers.ModelSerializer):
    class Meta:
        model = Przedmiot
        fields = '__all__'


class WypozyczenieSerializer(serializers.ModelSerializer):
    nazwa_przedmiotu = serializers.CharField(
        source="przedmiot.nazwa", read_only=True)
    imie_uzytkownika = serializers.CharField(
        source="uzytkownik.user.username", read_only=True)

    class Meta:
        model = Wypozyczenie
        fields = '__all__'

    def validate(self, data):
        """
        Check that start is before finish.
        """
        wypozyczenie = Wypozyczenie.objects.filter(przedmiot=data['przedmiot'])
        wypozyczenie = wypozyczenie.lastest('wypozyczenieZakonczenie')
        if data['wypozyczeniePoczatek'] > data['wypozyczenieZakonczenie']:
            raise serializers.ValidationError(
                {"wypozyczeniePoczatek": 'Data rozpoczecia nie moze byc mniejsza od daty zakończenia'})

        elif data['wypozyczeniePoczatek'] < data['przedmiot'].dostepnoscPoczatek:
            raise serializers.ValidationError(
                {"wypozyczeniePoczatek": 'Data wypozyczenia nie moze byc przed data dostepnosci'})

        elif data['wypozyczenieZakonczenie'] > data['przedmiot'].dostepnoscZakonczenie:
            raise serializers.ValidationError(
                {"wypozyczenieZakonczenie": 'Data oddania nie moze byc po zakończeniu dostepnosci'})
        elif data['wypozyczeniePoczatek'] < wypozyczenie.wypozyczenieZakonczenie:
            raise serializers.ValidationError(
                {"wypozyczeniePoczatek": 'Przedmiot jest juz wypozyczony w tym terminie'})
        return data


class OpiniaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opinia
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    # , queryset=Uzytkownik.objects.all())
    miasto = serializers.CharField(source='uzytkownik.miasto')
    # , queryset=Uzytkownik.objects.all())
    dataUrodzenia = serializers.DateField(source='uzytkownik.dataUrodzenia')

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2',
                  'first_name', 'last_name', 'miasto', 'dataUrodzenia')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()
        uzytkownik_data = validated_data['uzytkownik']
        print('*******\n\n\n\n')
        print("DATA URODZENIA: ", uzytkownik_data)
        print('*******\n\n\n\n')
        uzytkownik = Uzytkownik.objects.create(user=user, dataUrodzenia=uzytkownik_data['dataUrodzenia'],
                                               miasto=uzytkownik_data['miasto'])
        uzytkownik.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(**attrs)
        print("*****\n\n")
        print("ATTR", attrs)
        print("USER: ", user)
        print("ALL USERS", User.objects.all())
        print("*****\n\n")
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Złe dane logowania")
