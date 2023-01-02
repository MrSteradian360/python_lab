# to nie jest zadanie na jeden plik

import datetime
import pickle
import os
from datetime import datetime, timedelta


class Book:
    def __init__(self, idx: int, title: str, author: str, available: str, borrowed_by: str, key_words: set[str],
                 reservation: str):
        self.idx = idx  # book index
        self.title = title
        self.author = author
        self.available = available  # date when book will be available; if now, available == 'dostępna'
        self.borrowed_by = borrowed_by  # who has the book; if no one, borrowed_by == None
        self.key_words = key_words
        self.reservation = reservation  # who reserved the book to borrow it next; if no one reservation == None
        self.extended = False  # is book borrowing being extended

    def __repr__(self):
        return str("idx: " + str(
            self.idx) + "; tytuł: '" + self.title + "'; autor: " + self.author +
                   "; wypożyczona do: " + self.available + "; słowa kluczowe: " + str(self.key_words))

    def borrow(self, user):
        date = datetime.now() + timedelta(days=30)  # extending the borrowing by 30 days
        self.available = str(date.date())
        self.borrowed_by = str(user)
        print("Wypożyczono książkę na 30 dni! Data oddania: " + self.available)  # komunikacja z użytkownikiem w metodzie, która raczej odpowiada za logikę biznesową

    def extend(self):
        date = datetime.strptime(self.available, '%Y-%m-%d')
        self.available = str((date + timedelta(days=30)).date())
        self.extended = True
        print("Przedłużono wypożyczenie o 30 dni! Data oddania: " + self.available)

    def reserve(self, user):
        self.reservation = user
        print("Pomyślnie zarezerwowano książkę! Książkę można odebrać " + self.available)

    def returned(self):
        self.available = 'dostępna'
        self.borrowed_by = None
        self.extended = False


class User:
    def __init__(self, firstname, lastname, login, password):
        self.password = password
        self.login = login
        self.lastname = lastname
        self.firstname = firstname


class Reader(User):
    def __init__(self, firstname, lastname, login, password, reader_idx):
        super().__init__(firstname, lastname, login, password)
        self.reader_idx = reader_idx

    def __repr__(self):
        return "Imię: "+ self.firstname + "; nazwisko: " + self.lastname + "; login: " + self.login +\
               "; hasło: " + self.password + "; indeks czytelnika: "+str(self.reader_idx)


class Worker(User):
    def __init__(self, firstname, lastname, login, password, worker_idx):
        super().__init__(firstname, lastname, login, password)
        self.worker_idx = worker_idx

    def __repr__(self):
        return "Imię: " + self.firstname + "; nazwisko: " + self.lastname + "; login: " + self.login + \
               "; hasło: " + self.password + "; indeks czytelnika: " + str(self.worker_idx)


def menu(options):
    options = list(options.items())
    while True:
        for ind, option in enumerate(options, start=1):
            print(f"{ind}. {option[0]}")
        try:
            choice = int(input("Podaj numer: "))
            if 0 < choice <= len(options):
                func, args, kwargs = options[choice - 1][1]
                return func(*args, **kwargs)
        except ValueError:
            pass  # pusty except wymaga komentarza


def logging_in(user_type):
    error = 0
    while error < 3:
        login = input("Podaj login: ")
        password = input("Podaj hasło: ")
        reader_credentials = {reader.login: reader.password for reader in readers}
        worker_credentials = {worker.login: worker.password for worker in workers}
        if user_type == 'c' and (login, password) in reader_credentials.items():
            print("Logowanie użytkownika zakończone sukcesem!")
            while True:
                menu({"Wypożycz książkę": (borrow_book, (login,), {}),
                      "Zarezerwuj wypożyczoną książkę": (reserve_book, (login,), {}),
                      "Przedłuż wypożyczenie": (extend, (login,), {}),
                      "Przeglądaj katalog": (search_catalog, (), {}),
                      "Wyjdź": (exit, (), {})})
        if user_type == 'b' and (login, password) in worker_credentials.items():
            print("Logowanie pracownika zakończone sukcesem!")
            while True:
                menu({"Zaakceptuj zwrot książki": (accept_return, (), {}),
                      "Dodaj nową książkę": (add_book, (), {}),
                      "Usuń książkę z systemu": (remove_book, (), {}),
                      "Dodaj czytelnika": (add_reader, (), {}),
                      "Przeglądaj katalog": (search_catalog, (), {}),
                      "Wyjdź": (exit, (), {})})
        else:
            print("Niepoprawne dane!")
            error += 1
    if error >= 3:
        print("Odnowa dostępu")
        exit()


def borrow_book(login):
    results = search()
    if results == -1:
        return
    else:
        print("Wybierz książkę")
        args = {}
        for result in results:
            if result.available == 'dostępna' and (result.reservation is None or result.reservation == login):
                args[repr(result)] = (result.borrow, (login,), {})
        args |= {"Powrót": (go_back, (), {})}
        menu(args)


def go_back():
    pass


def search():
    print("Jak chcesz znaleźć książkę?")
    results = menu({"Po tytule": (find_book, (0,), {}), "Po autorze": (find_book, (1,), {}),
                    "Po słowach kluczowych": (find_book, (2,), {})})
    if results == -1:
        return -1
    return results


def find_book(search_type):
    if search_type == 0:
        order = input("Podaj tytuł lub jego fragment: ")
        return find(order, 0)
    if search_type == 1:
        order = input("Podaj autora: ")
        return find(order, 1)
    if search_type == 2:
        order = input("Podaj słowo kluczowe: ")
        return find(order, 2)


def find(order, search_type):
    results = []
    if search_type == 0:
        for book in books:
            if order.lower() in book.title.lower():
                results.append(book)
    if search_type == 1:
        for book in books:
            if order.lower() in book.author.lower():
                results.append(book)
    if search_type == 2:
        keys = order.lower().split()
        for book in books:
            for key in keys:
                if key in book.key_words:
                    results.append(book)
                    break
    if results:
        return results
    print("Nie znaleziono podanej książki!")
    return -1


def reserve_book(login):
    args = {}
    print("Książki dostępne do rezerwacji:")
    for book in books:
        if book.borrowed_by is not None and book.reservation is None and book.borrowed_by != login:
            args[repr(book)] = (book.reserve, (login,), {})
    args |= {"Powrót": (go_back, (), {})}
    menu(args)


def extend(login):
    args = {}
    print("Wypożyczenie której książki chcesz przedłużyć?")
    for book in books:
        if book.borrowed_by == login and book.reservation is None and not book.extended:
            args[repr(book)] = (book.extend, (), {})
    args |= {"Powrót": (go_back, (), {})}
    menu(args)


def search_catalog():
    results = search()
    if results == -1:
        return
    else:
        print("Książki spełniające podane kryteria:")
        for result in results:
            print(result)
        menu({"Powrót": (go_back, (), {})})


def accept_return():
    try:
        idx = int(input("Podaj indeks zwróconej książki: "))
        for book in books:
            if idx == book.idx:
                book.returned()
                print("Zwrot zaakceptowany pomyślnie!")
                return
        print("Brak książki o podanym indeksie")
    except ValueError:
        print("Błędne dane")


def remove_book():
    try:
        idx = int(input("Podaj indeks książki do usunięcia: "))
        for book in books:
            if idx == book.idx:
                books.remove(book)
                print("Książka usunięta pomyślnie!")
                return
        print("Brak książki o podanym indeksie")
    except ValueError:
        print("Błędne dane")


def add_reader():
    try:
        reader_idx = input("Indeks czytelnika: ")
        for reader in readers:
            if reader.reader_idx == reader_idx:
                print("Podany indeks już istnieje!")
                return
        firstname = input("Imię czytelnika: ")
        lastname = input("Nazwisko czytelnika: ")
        login = input("Login czytelnika: ")
        for reader in readers:
            if reader.login == login:
                print("Podany login już istnieje!")
                return
        password = input("Hasło czytelnika: ")
        for reader in readers:
            if reader.password == password:
                print("Podane hasło już istnieje!")
                return
        reader = Reader(firstname, lastname, login, password, reader_idx)
        readers.add(reader)
        print("Czytelnik dodany pomyślnie!")
    except ValueError:
        print("Błędne dane")


def add_book():
    try:
        idx = int(input("Indeks: "))
        for book in books:
            if book.idx == idx:
                print("Podany indeks już istnieje!")
                return
        title = input("Tytuł: ")
        author = input("Autor: ")
        available = input("Data oddania (format rrrr-mm-dd)/ dostępna: ")
        if available != 'dostępna':
            datetime.strptime(available, '%Y-%m-%d')  # checking if date is correct
        borrowed_by = input("Wypożyczony przez: ")
        if borrowed_by == 'None':
            borrowed_by = None
        else:
            exists = False
            for reader in readers:
                if reader.login == borrowed_by:
                    exists = True
                    break
            if not exists:
                print("Nie ma takiego czytelnika!")
                return
        key_words = set(input("Słowa kluczowe: ").replace(',', '').split())
        reservation = input("Rezerwacja: ")
        if reservation == 'None':
            reservation = None
        else:
            if reservation == borrowed_by:
                print("Użytkownik nie może zarezerwować książki, którą ma obecnie wypożyczoną!")
                return
            exists = False
            for reader in readers:
                if reader.login == reservation:
                    exists = True
                    break
            if not exists:
                print("Nie ma takiego czytelnika!")
                return
        book = Book(idx, title, author, available, borrowed_by, key_words, reservation)
        books.append(book)
        print("Książka dodana pomyślnie!")
    except ValueError:
        print("Błędne dane")


def get_data():
    if os.path.isfile('./workers.pickle'):
        with open('./workers.pickle', "rb") as file:
            workers = pickle.load(file)
    else:
        workers = {Worker('Adam', 'Nowak', 'w', 'w', 1)}

    if os.path.isfile('./readers.pickle'):
        with open('./readers.pickle', "rb") as file:
            readers = pickle.load(file)
    else:
        readers = {Reader('Anna', 'Kowalska', 'u', 'u', 1)}

    if os.path.isfile('./books.pickle'):
        with open('./books.pickle', "rb") as file:
            books = pickle.load(file)
    else:
        books = [
            Book(0, 'Pan Tadeusz', 'Adam Mickiewicz', 'dostępna', None, {'ksiądz', 'litwa', 'niepodległość', 'państwo'},
                 None),
            Book(1, 'Pan Tadeusz', 'Adam Mickiewicz', '2023-10-13', 'u',
                 {'ksiądz', 'litwa', 'niepodległość', 'państwo'}, None),
            Book(2, 'Balladyna', 'Juliusz Słowacki', 'dostępna', None, {'siostry', 'zdrada', 'maliny', 'piorun'}, None),
            Book(3, 'Makbet', 'William Szekspir', '2023-10-13', 'u', {'król', 'władza', 'zdrada', 'przepowiednia'},
                 None),
            Book(4, 'Romeo i Julia', 'William Szekspir', 'dostępna', None, {'miłość', 'konflikt', 'trucizna'}, None),
            Book(5, 'Romeo i Julia', 'William Szekspir', 'dostępna', None, {'miłość', 'konflikt', 'trucizna'}, None)]
    return workers, readers, books


def save_data():
    with open('./workers.pickle', "wb") as file:
        pickle.dump(workers, file)
    with open('./readers.pickle', "wb") as file:
        pickle.dump(readers, file)
    with open('./books.pickle', "wb") as file:
        pickle.dump(books, file)


if __name__ == '__main__':
    workers, readers, books = get_data()
    try:
        menu({"Zaloguj się":
                  (menu, ({
                              "Czytelnik":
                                  (logging_in, 'c', {}),
                              "Bibliotekarz":
                                  (logging_in, 'b', {}),
                              "Wyjdź": (exit, (), {})
                          },), {}), "Wyjdź": (exit, (), {})})
    finally:
        save_data()
