from collections import UserDict
from datetime import datetime
import pickle 

class Field:    
    def __init__(self, value=None):
        self._value = value

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value

class Phone(Field):     
    def __init__(self, value=None):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if self.is_valid_phone(value):
            self._value = value
        else:
            raise ValueError(f"Неправильний формат телефона: {value}")

    def is_valid_phone(self, value):
        try:
            if len(value) == 12 and value.isdigit():
                return True
        except ValueError:
            return False
    
class Name(Field):
    pass

class Email(Field):    
    pass

class Birthday(Field):
    def __init__(self, value=None):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if self.is_valid_date(value):
            self._value = value
        else:
            raise ValueError(f"Неправильний формат дати: {value}")

    def is_valid_date(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return True
        except ValueError:
            return False

class Record:
    def __init__(self, name: str, phones: list, emails: list, birthday=None):
        self.name = name
        self.phones = phones
        self.emails = emails
        self.birthday = birthday

    def days_until_birthday(self):
        if self.birthday.value:
            today = datetime.today().date()
            birthday = datetime.strptime(self.birthday.value, "%d.%m.%Y").date()

            next_birthday = birthday.replace(year=today.year)
            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)

            days_left = (next_birthday - today).days
            return days_left
        else:
            return None
           
    def add_phone(self, phone):
        phone_number = Phone(phone)
        if phone_number not in self.phones:
            self.phones.append(phone_number)

    def add_email(self, email):
        email_adress = Email(email)
        if email_adress not in self.emails:
            self.emails.append(email_adress)

    def find_phone(self, value):
        pass

    def delete_phone(self, phone):
        if phone in self.phones:
            index = self.phones.index(phone)
            self.phones.remove(phone)
            return index
        else:
            return None

    def edit_phone(self, old_phone, new_phone):
        if old_phone in self.phones:
            index = self.phones.index(old_phone)
            self.phones[index] = new_phone
            return index
        else:
            return None       
 

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find_record(self, value):
        return self.data.get(value)
            
    def iterator(self, N):
        count = 0
        views = []
        
        for name, record in self.data.items():
            phone_str = ", ".join(phone.value for phone in record.phones)
            email_str = ", ".join(email.value for email in record.emails)
            birthday_str = record.birthday.value if record.birthday is not None else "N/A"
            views.append(f"Name: {name}, Phones: {phone_str}, Emails: {email_str}, Birthday: {birthday_str}")
            count += 1
            if count == N:
                yield "; ".join(views)
                count = 0
                views = []

        if views:
            yield "\n".join(views)

    def save_to_file(self, filename):      # Запис у файл за протоколом pickle
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename):    # Завантаження з файлу за протоколом pickle
        try:
            with open(filename, 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            print("Файл не зайдено")
        except Exception as error:
            print(f"Виникла помилка: {error}")

   
    def search(self, search_str: str):
        result = []
        for name, record in self.data.items():                  
            result.append(name) if search_str.lower() in name.lower() else None
            for email in record.emails:
                if name not in result:                                     
                    result.append(name) if search_str.lower() in email.value.lower() else None
            for phone in record.phones:
                if name not in result:                                 
                    result.append(name) if search_str in phone.value else None
        return result

if __name__ == '__main__':
    
    addressbook = AddressBook()
    
    def init_contact():
        rec = Record(name, all_phones, all_emails, birthday)
        addressbook.add_record(rec)
        return rec
    
    def print_contact(rec):
        print("Ім'я:", rec.name.value)
        print("Телефони:", ', '.join(tel.value for tel in all_phones))
        print("Emails:", ', '.join(email.value for email in all_emails))
        if rec.birthday.value:
            print("День народження:", rec.birthday.value)
            print("До дня народження:", rec.days_until_birthday(), "днів")

    try:
        name = Name("Andrew")
        phone1 = Phone()
        phone1.value = "380671234455"
        phone2 = Phone()
        phone2.value = "380503216677"
        all_phones = [phone1, phone2]
        email = Email('andrew@gmail.com')
        all_emails = [email]
        birthday = Birthday()
        birthday.value = "18.08.2003"
        rec = init_contact()
        # print_contact(rec)

        name = Name("Sergii")
        phone1 = Phone()
        phone1.value = "380673451270"
        phone2 = Phone()
        phone2.value = "380502321517"
        all_phones = [phone1, phone2]
        email = Email('sergii@gmail.com')
        all_emails = [email]
        birthday = Birthday()
        birthday.value = "21.07.1999"
        rec = init_contact()
        # print_contact(rec)

        name = Name("Oleg")
        phone1 = Phone()
        phone1.value = "380938761535"
        phone2 = Phone()
        phone2.value = "380502329870"
        all_phones = [phone1, phone2]
        email = Email('oleg@gmail.com')
        all_emails = [email]
        birthday = Birthday()
        birthday.value = "17.02.2004"
        rec = init_contact()
        # print_contact(rec)

        name = Name("Olga")
        phone1 = Phone()
        phone1.value = "380933458790"
        phone2 = Phone()
        phone2.value = "380507778899"
        all_phones = [phone1, phone2]
        email1 = Email('olga@gmail.com')
        email2 = Email('olga@yahoo.com')
        all_emails = [email1, email2]
        birthday = Birthday()
        # birthday.value = "16.03.2001"
        rec = init_contact()
        # print_contact(rec)

        N=1 # Кількість записів для виводу за одну ітерацію
        
        for views in addressbook.iterator(N):
            print(views)

    except ValueError as error:
        print(error)

    # Збереження адресної книги у файл
    addressbook.save_to_file('addressbook.pkl')

    # Відновлення адресної книги з файла
    loaded_addressbook = AddressBook()
    loaded_addressbook.load_from_file('addressbook.pkl')

    # Перевірка відновленої з файла адресної книги
    print('\n')
    for name, record in loaded_addressbook.items():
        phones = [phone.value for phone in record.phones]
        emails = [email.value for email in record.emails]
        print(name, phones, emails, record.birthday.value if record.birthday else '')

    # Пошук в адресній книзі
    while True:
        print('\n')
        search_str = input('Введіть рядок для пошуку("Enter" для завершення) >> ')
        if search_str == '':
            break
        found = loaded_addressbook.search(search_str)
        print(found) if found else print('Нікого не знайдено')