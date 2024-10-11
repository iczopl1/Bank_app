import sqlite3
import csv
#plik csv
plik_z_danymi = "dane_uzytkownikow.csv"
#deklaracja zmiennej bazy danych
db_instancja = None
# funkcja odpowiedzialna za otrzymywanie dostępu do tej samej bazy danych w różnych plikach 
def get_db_instance():
    global db_instancja
    if db_instancja is None:
        db_instancja = Database()
    return db_instancja


class Database:
    def __init__(self, db_file='baza_danych_SQLlite.db'):
        # Deklaracja bazy danych i wczytanie danych z pliku
        self.baza_danych = sqlite3.connect(db_file)
        self.cursor = self.baza_danych.cursor()
        self.stworz_tabele()
    
    def stworz_tabele(self):
        # Tworzenie tabeli w bazie danych
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                imie TEXT NOT NULL,
                nazwisko TEXT NOT NULL,
                login TEXT UNIQUE NOT NULL,
                haslo TEXT NOT NULL,
                nr_telefonu TEXT,
                stan_konta INTEGER 
            )
        ''')
        # Zatwierdzenie stworzenia tabeli
        self.baza_danych.commit()

    def zapisz_do_bazy(self, imie, nazwisko, login, haslo, nr_telefonu, stan_konta):
        self.cursor.execute('''
            INSERT INTO users (imie, nazwisko, login, haslo, nr_telefonu, stan_konta)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (imie, nazwisko, login, haslo, nr_telefonu, stan_konta))
        self.baza_danych.commit()

    # Blok aktualizujący dane ---------------------------------------------------------------------------------
    def aktualizuj_stan_konta(self, login, nowy_stan):
        self.cursor.execute('''
            UPDATE users SET stan_konta = ? WHERE login = ?
        ''', (nowy_stan, login))
        self.baza_danych.commit()

    def zmien_haslo(self, login, nowe_haslo):
        self.cursor.execute('''
            UPDATE users SET haslo = ? WHERE login = ?
        ''', (nowe_haslo, login))
        self.baza_danych.commit()

    def zmien_imie(self, login, nowe_imie):
        self.cursor.execute('''
            UPDATE users SET imie = ? WHERE login = ?
        ''', (nowe_imie, login))
        self.baza_danych.commit()

    def zmien_nazwisko(self, login, nowe_nazwisko):
        self.cursor.execute('''
            UPDATE users SET nazwisko = ? WHERE login = ?
        ''', (nowe_nazwisko, login))
        self.baza_danych.commit()

    def zmien_tel(self, login, nowe_tel):
        self.cursor.execute('''
            UPDATE users SET nr_telefonu = ? WHERE login = ?
        ''', (nowe_tel, login))
        self.baza_danych.commit()

    #Koniec bloku aktualizującego dane ------------------------------------------------------------------------
    #------------Funkcje zarządzania bazą-----------------------------------------------------
    def zaloguj(self,login, haslo)->str:
        """_summary_

        Args:
            login (str): Login do zalogowania
            haslo (str): Hasło dozalogowania

        Returns:
            str: login zalogowanego urzytkownika w teori powinienn to być sekretny kod id 
        """
        self.cursor.execute('''
            SELECT login FROM users WHERE login = ? AND haslo = ?
        ''', (login, haslo))
        wynik = self.cursor.fetchone()

        if wynik:
            return wynik[0]
        else:
            return False
        
    def czy_istnieje_konto_o_loginie(self, login):
        self.cursor.execute('''
            SELECT nazwisko FROM users WHERE login = ?
        ''', (login,))  # przekazanie loginu do polecenia select
        wynik = self.cursor.fetchone()

        if wynik is None:
            return False  
        return wynik[0]

    def odczyt_danych_konkretnego_user(self, user)->list:
        """Zwraca wszystkie dane urzytkownika

        Args:
            user (str): login do user

        Returns:
            list:
                'id':wunik[0]
                'imie': wynik[1],
                'nazwisko': wynik[2],
                'login': wynik[3],
                'haslo': wynik[4],
                'nr_telefonu': wynik[5],
                'stan_konta': wynik[6]

        """
        self.cursor.execute('''
            SELECT id, imie, nazwisko, login, haslo, nr_telefonu, stan_konta FROM users WHERE login = ?
        ''', (user,))  # przekazanie loginu do polecenia select
        wynik = self.cursor.fetchone()

        if wynik is None:
            return None  #Jakby coś poszło nie tak

        return {
            'id': wynik[0],
            'imie': wynik[1],
            'nazwisko': wynik[2],
            'login': wynik[3],
            'haslo': wynik[4],
            'nr_telefonu': wynik[5],
            'stan_konta': wynik[6]
        }
        
        
    def odczyt_uzytkownikow(self):
        self.cursor.execute('SELECT imie, nazwisko, login, nr_telefonu, stan_konta, id FROM users')
        wszystkie_dane = self.cursor.fetchall()

        uzytkownicy = []
        for wynik in wszystkie_dane:
            uzytkownicy.append({
                'id': wynik[5],
                'imie': wynik[0],
                'nazwisko': wynik[1],
                'login': wynik[2],
                'nr_telefonu': wynik[3],
                'stan_konta': wynik[4]
            })

        return uzytkownicy
    
    def licz_uzytkownik(self):
        # Zapytanie SQL, które liczy wszystkie rekordy w tabeli users
        self.cursor.execute('SELECT COUNT(*) FROM users')
        
        # Pobieranie wyniku
        liczba_uzytkownikow = self.cursor.fetchone()[0]
        
        return liczba_uzytkownikow


    #-----------Koniec tych funkcji---------------------------------------------------------------------------

    #-------Blok zapisu bazy ----------------------------------------------------------------------
    def zapisz_baze(self):
        try:
            self.baza_danych.commit()
            print("Zmiany zostały zapisane w bazie danych.")
            self.eksportuj_do_csv()
        except Exception as e:
            print(f"Błąd zapisu do bazy danych: {e}")

    def dodaj_dane_z_csv_do_bazy(self):
        try:
            with open(plik_z_danymi, newline='', encoding='UTF-8') as plik_csv:
                reader = csv.reader(plik_csv)
                next(reader)  # Pomijanie nagłówków

                for wiersz in reader:
                    id, imie, nazwisko, login, haslo, nr_telefonu, stan_konta = wiersz
                    self.zapisz_do_bazy(imie, nazwisko, login, haslo, nr_telefonu, int(stan_konta))

            print(f"Dane z pliku {plik_z_danymi} zostały dodane do bazy danych.")

        except Exception as e:
            print(f"Błąd podczas dodawania danych do bazy: {e}")

    def eksportuj_do_csv(self):
        nazwa_pliku = plik_z_danymi
        try:
            self.cursor.execute('SELECT * FROM users')
            dane = self.cursor.fetchall()

            with open(nazwa_pliku, 'w', newline='', encoding='UTF-8') as plik_csv:
                writer = csv.writer(plik_csv)
                writer.writerow(['ID', 'Imię', 'Nazwisko', 'Login', 'Hasło', 'Nr Telefonu', 'Stan Konta'])
                writer.writerows(dane)

            print(f"Dane zostały wyeksportowane do pliku {nazwa_pliku}")

        except Exception as e:
            print(f"Błąd podczas eksportowania danych: {e}")
    #---------------------------------------------------------------------------------------------------

    def close(self):
        self.baza_danych.commit()
        self.baza_danych.close()
        
    def commit(self):
        self.baza_danych.commit()