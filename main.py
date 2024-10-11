import tkinter as tk
from tkinter import *
from Zarzadzanie_danymi import get_db_instance

db = get_db_instance()

db.dodaj_dane_z_csv_do_bazy()

#domyślne kolory dla tekstów i tła
backgrand_color = '#333333'
foregrand_color = '#FFFFFF'

class Gui_bank(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("System Bankowy")
        self.geometry("650x400")
        self.user = None  # Użytkownik po zalogowaniu
        self.configure(bg='#333333')
        self.create_widgets()
    def create_widgets(self):
        self.label = tk.Label(self, text="Witaj w systemie bankowym",bg=backgrand_color, fg=foregrand_color, font=('Aria, 20'))
        self.label.pack(pady=20)

        self.login_button = tk.Button(self, text="Zaloguj się", command=self.logowanie, bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        self.login_button.pack(pady=10)

        self.quit_button = tk.Button(self, text="Wyjdź", command=self.quit, bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        self.quit_button.pack(pady=10)

    def logowanie(self):
        self.clear_widgets()
        
        frame = tk.Frame(bg = backgrand_color)
        
        Zaloguj_napis = tk.Label(frame, text='Zaloguj' , bg=backgrand_color,fg=foregrand_color, font=('Aria, 30'))
        Login_napis = tk.Label(frame , text='Login', bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        self.Login_entry = Entry(frame, width= 20,font=('Aria, 16'))
        Haslo_napis = tk.Label(frame, text='Hasło', bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        self.Haslo_entry = Entry(frame, width=20, show='*', font=('Aria, 16'))
        Login_Button = Button(frame, text = 'Zaloguj', command=self.loguj, bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        Wyjdz_Button = Button(frame, text = 'Wyjdz', command=self.quit, bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        
        frame.pack()
        Zaloguj_napis.grid(column=0,row=0,columnspan=2, sticky='news', pady=30)
        Login_napis.grid(column=0,row=1,pady=10)
        self.Login_entry.grid(column=1,row=1)
        Haslo_napis.grid(column=0,row=2,pady=10)
        self.Haslo_entry.grid(column=1,row=2)
        Login_Button.grid(row=3,column=0,columnspan=2,pady=30)
        Wyjdz_Button.grid(row=4,column=0,columnspan=2,pady=5)
        
    def loguj(self):
        login = self.Login_entry.get()
        haslo = self.Haslo_entry.get()
        if login and haslo:
            user = db.zaloguj(login, haslo)
            if user:
                self.user = db.odczyt_danych_konkretnego_user(user)
                self.user_panel()
            else:
                self.bledne_logowanie()
        else:
            self.bledne_logowanie()


    def bledne_logowanie(self):
        self.clear_widgets()
        frame = tk.Frame(bg = backgrand_color)
        
        Bledne_dane_lable = tk.Label(frame, text='Wprowadzono błędne dane logowania' , bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        Back_Button = Button(frame, text = 'Cofnij', command=self.logowanie,bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        
        frame.pack()
        Bledne_dane_lable.grid(row=0,column=0)
        Back_Button.grid(row=1,column=0,pady=10)

    def user_panel(self):
        self.clear_widgets()
        frame = tk.Frame(bg = backgrand_color)
        
        Powitanie_label = tk.Label(frame, text=f'Witaj {self.user['imie']}' , bg=backgrand_color,fg=foregrand_color, font=('Aria, 30'))
        Zmien_dane_button = tk.Button(frame, text="Zmien swoje dane", command=self.zmien_dane,bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        Wplata_button = tk.Button(frame, text="Wpłata", command=self.wplata,bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        Wyplata_button = tk.Button(frame, text="Wypłata", command=self.wyplata,bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        Wykonaj_przelew_button = tk.Button(frame , text="Wykonaj przelew", command=self.wykonaj_przelew,bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        Logout_button = tk.Button(frame, text="Wyloguj", command=self.logout,bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        
        frame.pack()
        Powitanie_label.grid(row=0,column=0,pady=10,columnspan=2)
        Zmien_dane_button.grid(row=1,column=0,pady=10,columnspan=2)
        Wplata_button.grid(row=2,column=0)
        Wyplata_button.grid(row=2,column=1,pady=10)
        Wykonaj_przelew_button.grid(row=4,column=0,pady=10,columnspan=2)
        Logout_button.grid(row=5,column=0,pady=20,columnspan=2)

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    def zmien_dane(self):
        self.clear_widgets()
        self.user = db.odczyt_danych_konkretnego_user(self.user['login'])
        frame = tk.Frame(bg = backgrand_color)
        Opis_label = tk.Label(frame,text=f"Zmiana danych.Co chcesz zmienić?",bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        Aktualne_dane_label = tk.Label(frame,text=f"Aktualne dane:{self.user['imie']} {self.user['nazwisko']} {self.user['nr_telefonu']}",bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        Imie_zmien_button = tk.Button(frame, text="Zmien imie", command=lambda:self.zmien_dane_wybrane('imie'),bg=backgrand_color,fg=foregrand_color, font=('Aria, 16')) # dlaczego zaczoł zapentalać się program w tym miejscu
        Nazwisko_zmien_button  = tk.Button(frame, text="Zmien nazwisko", command=lambda:self.zmien_dane_wybrane('nazwisko'),bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        Nr_tel_zmien_button  = tk.Button(frame, text="Zmien numer telefonu", command=lambda:self.zmien_dane_wybrane('nr_tel'),bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        Haslo_zmien_button  = tk.Button(frame , text="Zmien haslo", command=lambda:self.zmien_dane_wybrane('haslo'),bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        Cofnij_button = tk.Button(frame, text="Cofnij", command=self.user_panel,bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        
        
        frame.pack()
        Opis_label.grid(row=0,column=0,pady=10,columnspan=2)
        Aktualne_dane_label.grid(row=1,column=0,columnspan=2)
        Imie_zmien_button.grid(row=2,column=0,pady=10)
        Nazwisko_zmien_button.grid(row=2,column=1)
        Nr_tel_zmien_button.grid(row=4,column=0,pady=10)
        Haslo_zmien_button.grid(row=4,column=1,)
        Cofnij_button.grid(row=5,column=0,pady=20,columnspan=2)
        
    def zmien_dane_wybrane(self,co):
        self.clear_widgets()
        match co:
            case 'imie':
                Funkcja = 'Wybrano zmiane imienia'
                Stara_dana = f'Stare imie to {self.user['imie']}'
                Wprowadz_nowe = 'Wprowadz nowe imie'
            case 'nazwisko':
                Funkcja = 'Wybrano zmiane nazwiska'
                Stara_dana = f'Stare nazwisko to {self.user['nazwisko']}'
                Wprowadz_nowe = 'Wprowadz nowe nazwisko'
            case 'nr_tel':
                Funkcja = 'Wybrano zmiane numeru telefonu'
                Stara_dana = f'Stary numer telefonu to {self.user['nr_telefonu']}'
                Wprowadz_nowe = 'Wprowadz nowy numer telefonu'
            case 'haslo':
                Funkcja = 'Wybrano zmianę hasła'
                Stara_dana = f'Wprowadz stare hasło by kontynuować'
                Wprowadz_nowe = 'Podaj hasło'
        
        frame = tk.Frame(bg = backgrand_color)
        
        Funkcja_napis = tk.Label(frame, text=Funkcja , bg=backgrand_color,fg=foregrand_color, font=('Aria, 30'))
        Stara_dana_napis = tk.Label(frame , text=Stara_dana, bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        Nowa_dana_napis = tk.Label(frame , text=Wprowadz_nowe, bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        self.Nowa_dana_entry = Entry(frame, width= 20,font=('Aria, 16'))
        if co =='haslo':
            Nowe_haslo_napis = tk.Label(frame , text="Podaj nowe haslo", bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
            self.Nowe_haslo_entry = Entry(frame, width= 20,font=('Aria, 16'))
        Potwierdz_Button = Button(frame, text = 'Zapisz zmiane', command=lambda:self.zapisz_zmiany(co), bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        Cofnij_Button = Button(frame, text = 'Cofnij', command=self.zmien_dane, bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        
        frame.pack()
        Funkcja_napis.grid(column=0,row=0,columnspan=2, sticky='news', pady=30)
        Stara_dana_napis.grid(column=0,row=1,pady=10,columnspan=2)
        Nowa_dana_napis.grid(column=0,row=2)
        self.Nowa_dana_entry.grid(column=1,row=2,pady=10)
        if co =='haslo':
            Nowe_haslo_napis.grid(column=0,row=3)
            self.Nowe_haslo_entry.grid(column=1,row=3,pady=10)
            Potwierdz_Button.grid(column=0,row=4)
            Cofnij_Button.grid(row=4,column=1,pady=30)
        else:
            Potwierdz_Button.grid(column=0,row=3)
            Cofnij_Button.grid(row=3,column=1,pady=30)
        
    def zapisz_zmiany(self,co):
        match co:
            case 'imie':
                imie= self.Nowa_dana_entry.get()
                db.zmien_imie(self.user['login'], imie)
                db.zapisz_baze()
                self.zmien_dane()
            case 'nazwisko':
                nazwisko= self.Nowa_dana_entry.get()
                db.zmien_nazwisko(self.user['login'],nazwisko)
                db.zapisz_baze()
                self.zmien_dane()
            case 'nr_tel':
                nr_tel= self.Nowa_dana_entry.get()
                db.zmien_tel(self.user['login'],nr_tel)
                db.zapisz_baze()
                self.zmien_dane()
            case 'haslo':
                stare_haslo= self.Nowa_dana_entry.get()
                if stare_haslo == self.user['haslo']:
                    nowe_haslo = self.Nowe_haslo_entry.get()
                    if len(nowe_haslo)>3:
                        db.zmien_haslo(self.user['login'],nowe_haslo)
                        db.zapisz_baze()
                        self.zmien_dane()
                    else:
                        self.wrong_password()
                else:
                    self.wrong_password()
        
    def wrong_password(self):
        self.clear_widgets()
        frame = tk.Frame(bg = backgrand_color)
        
        Bledne_dane_lable = tk.Label(frame, text='Wprowadzono błędne stare hasło albo nowe hasło jest za krutkie' , bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        Back_Button = Button(frame, text = 'Cofnij', command=self.zmien_dane,bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        
        frame.pack()
        Bledne_dane_lable.grid(row=0,column=0)
        Back_Button.grid(row=1,column=0,pady=10)
    
    def wplata(self):
        self.clear_widgets()
        frame = tk.Frame(bg = backgrand_color)
        
        Aktualny_stan_konta_label = tk.Label(frame, text=f'Stan konta: {self.user['stan_konta']}', bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        Wplata_lable = tk.Label(frame, text='Podaj kwotę wpłaty' , bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        self.Wplata_entry = Entry(frame, width= 20,font=('Aria, 16'))
        Zatwiedz_Button= Button(frame, text = 'Zatwierdz wpłatę', command=self.wplata_zatwierdz,bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        Back_Button = Button(frame, text = 'Cofnij', command=self.user_panel,bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        
        frame.pack()
        Aktualny_stan_konta_label.grid(row=0,column=0,pady=10)
        Wplata_lable.grid(row=1,column=0)
        self.Wplata_entry.grid(row=2,column=0,pady=10)
        Zatwiedz_Button.grid(row=3,column=0,pady=10)
        Back_Button.grid(row=4,column=0,pady=10)
            
    def wplata_zatwierdz(self):
        Wplata = self.Wplata_entry.get()
        nowy_stan = self.user['stan_konta']  + int(Wplata)
        db.aktualizuj_stan_konta(self.user['login'], nowy_stan)
        db.zapisz_baze()
        
        self.clear_widgets()
        frame = tk.Frame(bg = backgrand_color)
        Aktualny_stan_konta_label = tk.Label(frame, text=f'Nowy stan konta: {nowy_stan}'  , bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        Zatwiedz_Button= Button(frame, text = 'OK', command=self.user_panel,bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        
        frame.pack()
        Aktualny_stan_konta_label.grid(row=0,column=0,pady=10)
        Zatwiedz_Button.grid(row=1,column=0,pady=10)

    def wyplata(self):
        self.clear_widgets()
        frame = tk.Frame(bg = backgrand_color)
        
        Aktualny_stan_konta_label = tk.Label(frame, text=f'Stan konta: {self.user['stan_konta']}' , bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        Wplata_lable = tk.Label(frame, text='Podaj kwotę wypłaty' , bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        self.Wyplata_entry = Entry(frame, width= 20,font=('Aria, 16'))
        Zatwiedz_Button= Button(frame, text = 'Zatwierdz wypłatę', command=self.wyplata_zatwierdz,bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        Back_Button = Button(frame, text = 'Cofnij', command=self.user_panel,bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        
        frame.pack()
        Aktualny_stan_konta_label.grid(row=0,column=0,pady=10)
        Wplata_lable.grid(row=1,column=0)
        self.Wyplata_entry.grid(row=2,column=0,pady=10)
        Zatwiedz_Button.grid(row=3,column=0,pady=10)
        Back_Button.grid(row=4,column=0,pady=10)
            
    def wyplata_zatwierdz(self):
        Wyplata = int(self.Wyplata_entry.get())
        if self.user['stan_konta']<Wyplata:
            self.clear_widgets()
            frame = tk.Frame(bg = backgrand_color)
            Aktualny_stan_konta_label = tk.Label(frame, text=f'Brak środków do wypłaty' , bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
            Zatwiedz_Button= Button(frame, text = 'OK', command=self.user_panel,bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
            
            frame.pack()
            Aktualny_stan_konta_label.grid(row=0,column=0,pady=10)
            Zatwiedz_Button.grid(row=1,column=0,pady=10)
        else:
            nowy_stan = self.user['stan_konta']  - Wyplata
            db.aktualizuj_stan_konta(self.user['login'], nowy_stan)
            db.zapisz_baze()
            
            self.clear_widgets()
            frame = tk.Frame(bg = backgrand_color)
            Aktualny_stan_konta_label = tk.Label(frame, text=f'Nowy stan konta{nowy_stan}' , bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
            Zatwiedz_Button= Button(frame, text = 'OK', command=self.user_panel,bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
            
            frame.pack()
            Aktualny_stan_konta_label.grid(row=0,column=0,pady=10)
            Zatwiedz_Button.grid(row=1,column=0,pady=10)
    
    def wykonaj_przelew(self):
        self.clear_widgets()
        frame = tk.Frame(bg = backgrand_color)
        
        Wykonaj_przelew_label = tk.Label(frame, text='Wykonaj przelew' , bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        Podaj_odbiorce_lable = tk.Label(frame, text='Podaj login odbiorcy przelewu' , bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        self.Odbiorca_entry = Entry(frame, width= 20,font=('Aria, 16'))
        Sprawdz_odbiorce_Button= Button(frame, text = 'Sprawdz odbiorce', command=self.sprawdz_odbiorce,bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        Back_Button = Button(frame, text = 'Cofnij', command=self.user_panel,bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
        
        frame.pack()
        Wykonaj_przelew_label.grid(row=0,column=0,pady=10)
        Podaj_odbiorce_lable.grid(row=1,column=0)
        self.Odbiorca_entry.grid(row=2,column=0,pady=10)
        Sprawdz_odbiorce_Button.grid(row=3,column=0,pady=10)
        Back_Button.grid(row=4,column=0,pady=10)
            
    def sprawdz_odbiorce(self):
        # print(self.Odbiorca_entry) ----- najpierw poierz dane z wigetu a potem wyczyść pamietaj
        # print(self.Login_entry)
        szukany= self.Odbiorca_entry.get()
        self.clear_widgets()
        self.odbiorca_dane = None
        self.odbiorca_dane =db.odczyt_danych_konkretnego_user(szukany)
        if self.odbiorca_dane != None:
            frame = tk.Frame(bg = backgrand_color)
            
            Stan_odbiorcy_label = tk.Label(frame, text=f'Odbiorca o nazwisku {self.odbiorca_dane['nazwisko']} znaleziony w bazie' , bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
            Kwota_przelewu_lable = tk.Label(frame, text='Podaj kwotę przelewu' , bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
            self.Kwota_przelewu_entry = Entry(frame, width= 20,font=('Aria, 16'))
            Zatwierdz_przelew_Button= Button(frame, text = 'Zatwierdz_przelew', command=self.przeslij_przelew,bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
            Back_Button = Button(frame, text = 'Cofnij', command=self.user_panel,bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
            
            frame.pack()
            Stan_odbiorcy_label.grid(row=0,column=0,pady=10,columnspan=2)
            Kwota_przelewu_lable.grid(row=1,column=0)
            self.Kwota_przelewu_entry.grid(row=1,column=1,pady=10)
            Zatwierdz_przelew_Button.grid(row=2,column=0,pady=10,columnspan=2)
            Back_Button.grid(row=3,column=0,pady=10,columnspan=2)
        else:
            self.clear_widgets()
            frame = tk.Frame(bg = backgrand_color)
            Aktualny_stan_konta_label = tk.Label(frame, text=f'Nie znaleziono odbiorcy'  , bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
            Zatwiedz_Button= Button(frame, text = 'OK', command=self.user_panel,bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
            
            frame.pack()
            Aktualny_stan_konta_label.grid(row=0,column=0,pady=10)
            Zatwiedz_Button.grid(row=1,column=0,pady=10)
        
    def przeslij_przelew(self,):
        try:
            kwota = int(self.Kwota_przelewu_entry.get())
            if kwota <0:
                kwota = 0
        except:
            kwota = 0
        if self.user['stan_konta'] >= kwota:
            db.aktualizuj_stan_konta(self.user['login'], self.user['stan_konta'] - kwota)
            db.aktualizuj_stan_konta(self.odbiorca_dane['login'], self.odbiorca_dane['stan_konta'] + kwota)
            db.zapisz_baze()
            self.clear_widgets()
            frame = tk.Frame(bg = backgrand_color)
            Aktualny_stan_konta_label = tk.Label(frame, text=f'Przelano {kwota} do {self.odbiorca_dane['nazwisko']}'  , bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
            Zatwiedz_Button= Button(frame, text = 'OK', command=self.user_panel,bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
            
            frame.pack()
            Aktualny_stan_konta_label.grid(row=0,column=0,pady=10)
            Zatwiedz_Button.grid(row=1,column=0,pady=10)
        else:
            self.clear_widgets()
            frame = tk.Frame(bg = backgrand_color)
            Aktualny_stan_konta_label = tk.Label(frame, text=f'Nie wystarczające środki do wykonania przelewu'  , bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
            Zatwiedz_Button= Button(frame, text = 'OK', command=self.user_panel,bg=backgrand_color,fg=foregrand_color, font=('Aria, 16'))
            
            frame.pack()
            Aktualny_stan_konta_label.grid(row=0,column=0,pady=10)
            Zatwiedz_Button.grid(row=1,column=0,pady=10)

    def logout(self):
        self.user = None
        self.clear_widgets()
        self.create_widgets()




if __name__ == "__main__":
    app = Gui_bank()
    app.mainloop()