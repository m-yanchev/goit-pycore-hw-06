from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    # реалізація класу
	pass


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise PhoneNotValidError()
        super().__init__(value)


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone: str, new_phone: str):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                break
    
    def find_phone(self, phone: str) -> Phone | None:
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def remove_phone(self, phone: str):
        phone_obj = self.find_phone(phone)
        if phone_obj is not None:
            self.phones.remove(phone_obj)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]


class PhoneNotValidError(Exception):
    def __init__(self, message="Phone number must be 10 digits long and contain only numbers."):
        super().__init__(message)


# Створення нової адресної книги
book = AddressBook()
# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
# Додавання запису John до адресної книги
book.add_record(john_record)
# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)
# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)
# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")
print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555
# Пошук конкретного телефону в записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555
# Видалення запису Jane
book.delete("Jane")

# Спроба знайти видалений запис Jane
assert book.find("Jane") is None

# Спроба видалити неіснуючий телефон у записі John
john.remove_phone("0000000000")  # нічого не станеться

# Видалення існуючого телефону у записі John
john.remove_phone("1112223333")
print(john)  # Виведення: Contact name: John, phones: 5555555555
# Спроба знайти видалений телефон у записі John
assert john.find_phone("1112223333") is None

# Спроба додати некоректний телефон
try:
    john.add_phone("invalid_phone")
except PhoneNotValidError as e:
    print(e)  # Виведення: Phone number must be 10 digits long and contain only numbers.

