import csv
from faker import Faker
import random

# Inicjalizacja obiektu Faker
fake = Faker()

# Funkcja do generowania danych
def generuj_dane(num_records):
    records = []
    used_logins = set()  # Zestaw do przechowywania unikalnych loginów

    for i in range(num_records):
        # Generowanie fikcyjnych danych
        id_ = i + 3
        imie = fake.first_name()
        nazwisko = fake.last_name()

        # Generowanie unikalnego loginu
        login = fake.user_name()
        while login in used_logins:
            login = fake.user_name() + str(id)  # Generuj nowy login, jeśli już istnieje
        used_logins.add(login)  # Dodaj login do zestawu

        haslo = fake.password()
        nr_telefonu = fake.phone_number()
        stan_konta = random.randint(0, 100000)  # Losowy stan konta

        # Dodawanie rekordu do listy
        record = [id_, imie, nazwisko, login, haslo, nr_telefonu, stan_konta]

        # Sprawdzenie, czy rekord ma 7 wartości
        if len(record) != 7:
            print(f"Niepoprawny rekord: {record}. Oczekiwano 6 wartości.")
            continue  # Pomijanie niepoprawnych rekordów

        records.append(record)

    return records

# Zapis danych do pliku CSV
def zapisz_do_csv(nazwa_pliku, records):
    with open(nazwa_pliku, mode='w', newline='', encoding='utf-8') as plik_csv:
        writer = csv.writer(plik_csv)
        # Zapis nagłówków
        writer.writerow(['ID', 'Imię', 'Nazwisko', 'Login', 'Hasło', 'Nr Telefonu', 'Stan Konta'])
        writer.writerow(['1', 'Pawel', 'Nieistniejocy', 'iczo', '1234', '+48 324 435 345', '999666999'])
        writer.writerow(['2', 'Piotr', 'Kruczek', 'Piotr', '1234', '+48 324 435 345', '999666999'])
        # Zapis danych
        writer.writerows(records)

# Główna funkcja
if __name__ == '__main__':
    num_records = 100 # Liczba rekordów do wygenerowania
    dane = generuj_dane(num_records)
    zapisz_do_csv('dane_uzytkownikow.csv', dane)
    print(f'Wygenerowano {len(dane)} rekordów i zapisano do pliku dane_uzytkownikow.csv')
