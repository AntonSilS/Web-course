≠
from collections import UserDict, defaultdict
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import os.path
import pickle
import re


#from models import Contact, Phone
#from sqlalchemy.engine import create_engine
#from sqlalchemy.orm import sessionmaker
#from sqlalchemy.sql import select, update, delete, or_

from models_2 import Address, Birthday, ContactUser, Email, PhoneUser
import connect

from connect import URL
from pymongo import MongoClient


# --------------------------------Prompt Toolkit-------------------------------
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style

SqlCompleter = WordCompleter([
    'add', 'close', 'exit', 'save', 'remove', 'add address', 'add birthday', 'add email', 'add phone',
    'delete address', 'delete birthday', 'delete email', 'delete phone',
    'change email', 'change birthday', 'change address', 'change phone',
    'coming birthday', 'good bye', "add note", "find note", "change note",
    "delete note", "tag note", "help", 'show all', 'search', 'clean', 'show bd', 'search bd'], ignore_case=True)

style = Style.from_dict({
    'completion-menu.completion': 'bg:#008888 #ffffff',
    'completion-menu.completion.current': 'bg:#00aaaa #000000',
    'scrollbar.background': 'bg:#88aaaa',
    'scrollbar.button': 'bg:#222222',
})
# --------------------------------Prompt Toolkit-------------------------------


# --------------------------------WEB MODULE 2-------------------------------

class IMongoConnact():
    def __init__(self):
        client = MongoClient(URL)
        self.db = client['test']

    def add_name_bd(self):
        ContactUser(name=self.name, address=Address(addr=self.address),
                    birthday=Birthday(brth=self.birthday), email=Email(eml=self.email)).save()
    
        #ContactUser(name=self.name).save()
    
    def add_addr_bd(self):
        ContactUser.objects(name=self.name).update(address=Address(addr=self.address))

    def add_brth_bd(self):
        #date_brth = datetime.strptime(self.birthday, '%d.%m.%Y').date()
        ContactUser.objects(name=self.name).update(birthday=Birthday(brth=self.birthday))

    def add_eml_bd(self):
        ContactUser.objects(name=self.name).update(email=Email(eml=self.email))

    def add_phn_bd(self, phone):
        phone = self.check_phone(phone)
        #ContactUser.objects(name=self.name).update(push__phone=(PhoneUser(phn=phone)))
        ContactUser.objects(name=self.name).update(push__phone=(phone))
    
    def change_addr_bd(self):
        self.add_addr_bd()
    
    def change_brth_bd(self):
        self.add_brth_bd()
    
    def change_eml_bd(self):
        self.add_eml_bd()
    
    def change_phn_bd(self, phones):
        cur_phone = phones[0]
        new_phone = phones[1]
        ContactUser.objects(name=self.name).update(pull__phone=(PhoneUser(phn=cur_phone)))
        ContactUser.objects(name=self.name).update(push__phone=(PhoneUser(phn=new_phone)))
    
    def remove_name_bd(self):
        ContactUser.objects(name=self.name).delete()
    
    def delete_addr_bd(self):
        ContactUser.objects(name=self.name).update(unset__address=Address(addr=self.address))

    def delete_brth_bd(self):
        #date_brth = datetime.strptime(self.birthday, '%d.%m.%Y').date()
        ContactUser.objects(name=self.name).update(unset__birthday=Birthday(brth=self.birthday))
    
    def delete_eml_bd(self):
        ContactUser.objects(name=self.name).update(unset__email=Email(eml=self.email))
    
    def delete_phn_bd(self, phone):
        ContactUser.objects(name=self.name).update(pull__phone=(PhoneUser(phn=phone)))

    def bd_print(self, conts):
        to_show = []
        for con in conts:
            
            con_id = str(con['_id'])
            phones_list = con['phone']
            phones_str = ', '.join(phones_list)
            phones_str = "____" if not phones_list else phones_str
            con_name = con['name']
            con_email = "____" if not con['email'] else con['email']['eml']
            
            con_brth = "____" if not con['birthday'] else con['birthday']['brth']
            con_addr = "____" if not con['address'] else con['address']['addr']
            to_show.append(f'\n┌{"-" * 108}┐\
                            \n| Name: {con_name:<71} ID: {con_id:<24} |\
                            \n| Phones: {phones_str:<98} |\
                            \n| Email: {con_email:<70} Date of birth: {con_brth:<13} |\
                            \n| Address: {con_addr:<97} |\
                            \n└{"-" * 108}┘\n')
            #f'\n| Name: {con_name} |\old
                    #\n| ID: {con_id}|\
                    #\n| Address: {con_addr} | Birthday: {con_brth} |\
                    #\n| Email: {con_email} |\
                    #\n| Phones: {phones_str} |')
            
        return "\n".join(to_show)

    
    def srch_bd(self, command_line): 
        key = ' '.join(command_line).strip()
        result = self.db.contact_user.find({
            '$or': [
                { 'name': { '$regex': key, '$options': 'i' } },
                { 'address.addr': { '$regex': key, '$options': 'i' } },
                { 'birthday.brth': { '$regex': key, '$options': 'i' } },
                { 'email.eml': { '$regex': key, '$options': 'i' } },
                { 'phone': { '$in': [key] } }
                ]})
        if result:
            return self.bd_print(result)
        else: 
            return 'Database is empty'

        
    
    def shw_bd(self):
        res = self.db.contact_user.find({})
        if res: 
            return self.bd_print(res)
        else:
            return 'No records found.'




class ISqlLiteConnact():

    def __init__(self):
        self.name = None
        self.email = None
        engine = create_engine("sqlite:///myadd_book.db")#check how it works!!!
        Session = sessionmaker(bind=engine)#check how it works!!!
        self.session = Session()#check how it works!!!


    def get_cont_id(self, name):
        stmt = select(Contact.id).filter_by(con_name=name)
        con_id = self.session.execute(stmt).scalar()
        return con_id

    def add_name_bd(self):
        stmt = select(Contact.id, Contact.con_name).filter_by(con_name=self.name)
        result = self.session.execute(stmt).all()
        if not result:
            contact_name = Contact(con_name=self.name)
            self.session.add(contact_name)
            self.session.commit()

    def add_eml_bd(self):#work with instance of Record from contacts(ins. AddressBook)
        con_id = self.get_cont_id(self.name)
        if con_id:
            stmt = update(Contact).where(Contact.id==con_id).values(email=self.email)
            self.session.execute(stmt)
            self.session.commit()
        

    def add_phn_bd(self, phone):#work with instance of Record from contacts(ins. AddressBook)
        phone = self.check_phone(phone)
        con_id = self.get_cont_id(self.name)
        if con_id:
            phone_cont = Phone(description=phone, contact_id=con_id)#(0XX)XXX-XX-XX
            self.session.add(phone_cont)
            self.session.commit()

    def remove_name_bd(self):
        con_id = self.get_cont_id(self.name)
        if con_id:
            stmt = delete(Contact).where(Contact.id==con_id)
            stmt_phone = delete(Phone).where(Phone.contact_id==con_id)
            self.session.execute(stmt)
            self.session.execute(stmt_phone)
            self.session.commit()    
    
    def delete_eml_bd(self):
        con_id = self.get_cont_id(self.name)
        if con_id:
            stmt = update(Contact).where(Contact.id==con_id).values(email=None)
            self.session.execute(stmt)
            self.session.commit()

    def delete_phn_bd(self, phone):
        stmt = select(Phone.id, Contact).join(Phone).filter(Contact.con_name==self.name, Phone.description==phone)
        phone_id = self.session.execute(stmt).scalar()
        if phone_id:
            stmt = delete(Phone).where(Phone.id==phone_id)
            self.session.execute(stmt)
            self.session.commit()
    
    def change_eml_bd(self):
        self.add_eml()

    def change_phn_bd(self, phones):
        stmt = select(Phone.id, Contact).join(Phone).filter(Contact.con_name==self.name, Phone.description==phones[0])
        phone_id= self.session.execute(stmt).scalar()
        if phone_id:
            stmt = update(Phone).where(Phone.id==phone_id).values(description=phones[1])
            self.session.execute(stmt)
            self.session.commit()

    def bd_print(self, res_stmt): 
        to_show = []
        for con in res_stmt: 
            con_id = con[0]
            stmt_p = select(Phone.description).filter_by(contact_id=con_id)
            phones_list = self.session.execute(stmt_p).scalars().all()
            phones_str = ', '.join(phones_list)
            phones_str = "____" if not phones_list else phones_str

            con_name = con[1]
            con_email = "____" if con[2] == None else con[2]

            to_show.append(f'| ID: {con_id} | Name: {con_name} | Email: {con_email} | Phones: {phones_str} |')
        return "\n".join(to_show)


    def shw_bd(self):
        res = self.session.query(Contact.id, Contact.con_name, Contact.email).all()
        if res:
            return self.bd_print(res)
        else: 
            return 'Database is empty'
    
    def srch_bd(self, command_line):
        key = ' '.join(command_line).strip()
        res = self.session.query(Contact.id, Contact.con_name, Contact.email).\
                    join(Phone, isouter=True).\
                    filter(or_(Contact.con_name.like(f'%{key}%'),\
                                Phone.description.like(f'%{key}%'),\
                                Contact.email.like(f'%{key}%'))).group_by(Contact.id).all()
        if res: 
            return self.bd_print(res)
        else:
            return 'No records found.'

    

class IOutputeScreen(ABC):

    @abstractmethod
    def to_outpute(self):
        pass

class ToConsole(IOutputeScreen):

    def to_outpute(self, displayble_obj):
        return displayble_obj.display()


class ToWebsite(IOutputeScreen):

    def to_outpute(self, displayble_obj):
        pass
    

class IDisplayble(ABC):#new!!

    @abstractmethod
    def display(self):
        pass


class Note(IDisplayble):

    def __init__(self, note_text = ''):
        self.note_text = note_text
    
    def display(self):
        return self.note_text

class HelpList(IDisplayble):

    def __init__(self, text = ''):
        self.text = text
    
    def display(self):
        return self.text
# --------------------------------WEB MODULE 2-------------------------------


class CustomException(Exception):

    def __init__(self, text):
        self.txt = text

class AddressBook(UserDict, IDisplayble):

    def get_values_list(self):
        if self.data:
            return self.data.values()
        else:
            raise CustomException('Address book is empty.')

    def get_record(self, name):
        if self.data.get(name):
            return self.data.get(name)
        else:
            raise CustomException(
                'Such contacts doesn\'t exist.')

    def remove(self, name):
        if self.data.get(name):
            self.data.pop(name)
        else:
            raise CustomException(
                'Such contact  doesn\'t exist.')

    def load_from_file(self, file_name):
        if os.path.exists(file_name):
            with open(file_name, 'rb') as fh:
                self.data = pickle.load(fh)
                if len(self.data):
                    return f'The contacts book is loaded from the file "{file_name}".'
                else:
                    return "This is empty contacts book. Add contacts to it using the command 'add < NAME > '."
        else:
            return "This is empty contacts book. Add contacts into it using the command 'add <NAME>'."

    def save_to_file(self, file_name):
        with open(file_name, 'wb') as fh:
            pickle.dump(self.data, fh)
        return f'The contacts book is saved in the file "{file_name}".'

    def search(self, query):
        result = AddressBook()
        for key in self.data.keys():
            if query.lower() in str(self.get_record(key)).lower():
                match = self.get_record(key)
                result[key] = match
        if len(result) > 0:
            return f'{len(result)} records found:\n {result}'
        else:
            return f'No records found.'

    def __repr__(self):
        result = ""
        for key in self.data.keys():
            result += str(self.data.get(key))
        return result
# --------------------------------WEB MODULE 2-------------------------------
    def display(self):#new!!!
        return str(self)
# --------------------------------WEB MODULE 2-------------------------------

contacts = AddressBook()


class Record(IMongoConnact):

    def __init__(self, name, address=None, phones_list=None, email=None, birthday=None):
        self.name = name
        self._address = address
        self._phones_list = []
        self._email = email
        self._birthday = birthday
    
    def check_phone(self, phone):  
        if re.search('\(0\d{2}\)\d{3}-\d{2}-\d{2}', phone):
            return phone
        else: 
            raise CustomException(
                'Wrong phone number format! Use (0XX)XXX-XX-XX format!')

    def append_phone(self, phone):
        cor_phone = self.check_phone(phone)
        self._phones_list.append(cor_phone)

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = address

    def delete_address(self):
        self._address = None

    @property
    def phones_list(self):
        return self._phones_list

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if re.search('[a-zA-Z][\w.]+@[a-zA-z]+\.[a-zA-Z]{2,}', email):
            self._email = email
        else:
            raise CustomException(
                'Wrong email format! Correct format is aaaa@ddd.cc')

    def delete_email(self):
        self._email = None

    @property
    def birthday(self):
        return self._birthday

    @birthday.setter
    def birthday(self, birthday):
        if re.search('\d{2}\.\d{2}.\d{4}', birthday) and datetime.strptime(birthday, '%d.%m.%Y'):
            self._birthday = birthday
        else:
            raise CustomException(
                'Wrong date format! Correct format is DD.MM.YYYY')

    def delete_birthday(self):
        self._birthday = None

    def __repr__(self):
        name = self.name
        email = '---' if self.email == None else self.email
        address = '---' if self.address == None else self.address
        birthday = '---' if self.birthday == None else self.birthday
        if len(self.phones_list) == 0:
            phones = '---'
        else:
            phones = ', '.join(self.phones_list)
        return f'\n┌{"-" * 108}┐\n| {name:<51} Phones: {phones:<46} |\
                 \n| Email: {email:<73} Date of birth: {birthday:<10} |\
                 \n| Address: {address:<97} |\n└{"-" * 108}┘\n'


def input_error(func):

    def inner(command_line):
        try:
            result = func(command_line)
        except CustomException as warning_text:
            result = warning_text
        except Exception as exc:
            result = exc
            if func.__name__ == 'save_func':
                result = f'Error while saving.'
            elif func.__name__ == 'add_birthday':
                result = "Day out of range for this month."
            elif func.__name__ == 'coming_birthday' and exc.__class__.__name__ == "ValueError":
                result = "Use a number for getting list of birthdays more than next 7 days."
            elif func.__name__ == 'remove':
                pass
                #result = f'Error while removing record.'
            elif func.__name__ == 'change_address':
                result = f'Error while changing address.'
            elif func.__name__ == 'change_birthday':
                result = f'Error while changing birthday.'
            elif func.__name__ == 'change_email':
                result = f'Error while changing email.'
            elif func.__name__ == 'change_phone':
                pass
                #result = f'Error while changing phone.'
            elif func.__name__ == 'delete_address':
                pass
                #result = f'Error while deleting address.'
            elif func.__name__ == 'delete_birthday':
                result = f'Error while deleting birthday.'
            elif func.__name__ == 'delete_email':
                result = f'Error while deleting email.'
            elif func.__name__ == 'delete_phone':
                result = f'Error while deleting phone.'
            elif func.__name__ == 'search':
                result = f'Error while searching.'
        return result
    return inner


@input_error
def exit_func(command_line):
    return 'Good bye!'


@input_error
def save_func(command_line):
    return contacts.save_to_file('contacts.bin')


def prepare_value(command_line):
    if command_line:
        value = command_line.pop(-1)
        key = ' '.join(command_line)
        return key, value
    else:
        raise CustomException(
            'The command must be with INFORMATION you want to add or change (Format: <command> <name> <information>).')


def prepare_value_3(command_line):
    if command_line:
        key = ' '.join(command_line)
        value = input('Enter the address >>> ')
        return key, value
    else:
        raise CustomException(
            'The command must be in the format: <command> <name>.')


@input_error
def add_name(command_line):
    if command_line:
        name = ' '.join(command_line)
        if name in contacts.keys():
            raise CustomException(
                f'Contact with name "{name}" has been already added!!!!')
        else:
            record = Record(name)#old part
            contacts[name] = record#old part
            record.add_name_bd()#  mongo/sql
            return f'Contact with the name "{name}" has been successfully added.'
    else:
        raise CustomException(
            'The command must be with a NAME you want to add (Format: <add> <name>).')


@input_error
def add_address(command_line):
    key, address = prepare_value_3(command_line)
    contacts.get_record(key).address = address
    contacts.get_record(key).add_addr_bd()
    return f'Address {address} for the contact "{key}" has been successfully added.'


@input_error
def add_birthday(command_line):
    key, birthday = prepare_value(command_line)
    contacts.get_record(key).birthday = birthday
    contacts.get_record(key).add_brth_bd()
    return f'Date of birth {birthday} for the contact "{key}" has been successfully added.'


@input_error
def add_email(command_line):
    key, input_email = prepare_value(command_line)
    contacts.get_record(key).email = input_email#old part
    contacts.get_record(key).add_eml_bd()#sql/mongo |todo: change!!!
    return f'Email {input_email} for the contact "{key}" has been successfully added.'


@input_error
def add_phone(command_line):
    key, phone = prepare_value(command_line)
    if not phone in contacts.get_record(key).phones_list:
        contacts.get_record(key).append_phone(phone)#old part
        contacts.get_record(key).add_phn_bd(phone)#sql/mongo |todo: change!!!
        return f'Phone number {phone} for the contact "{key}" has been successfully added.'
    else:
        raise CustomException('Such phone number has been already added!')


def create_for_print(birthdays_dict):
    to_show = []
    for date, names in list(birthdays_dict.items()):
        to_show.append(
            f'{date.strftime("%A")}({date.strftime("%d.%m.%Y")}): {", ".join(names)}')
    if len(to_show) == 0:
        return f'There are no birthdays coming within this period.'
    else:
        return "\n".join(to_show)


@input_error
# можно задать другой диапазон вывода дней, по умолчанию 7
def coming_birthday(command_line):
    range_days = 7
    birthdays_dict = defaultdict(list)
    if command_line:
        range_days = int(command_line[0])
    current_date = datetime.now().date()
    timedelta_filter = timedelta(days=range_days)
    for name, birthday in [(i.name, i.birthday) for i in contacts.get_values_list()]:
        if name and birthday:  # проверка на None
            birthday_date = datetime.strptime(birthday, '%d.%m.%Y').date()
            current_birthday = birthday_date.replace(year=current_date.year)
            if current_date <= current_birthday <= current_date + timedelta_filter:
                birthdays_dict[current_birthday].append(name)
    return create_for_print(birthdays_dict)


@input_error
def search(command_line):
    #key, value = prepare_value(command_line)
    if command_line:
        return contacts.search(' '.join(command_line).strip())
    else:
        return 'Specify the search string.'


@input_error
def remove(command_line):
    key = ' '.join(command_line).strip()
    if contacts.get_record(key):
        contacts.get_record(key).remove_name_bd()#sql/mongo |todo: change!!!
        contacts.remove(key)#old part
        return f'Contact "{key}" has been successfully removed.'
    else:
 
        raise CustomException('Such contact does not exist!!!')


@input_error
def delete_address(command_line):
    key = ' '.join(command_line).strip()
    if key in contacts.keys():
        address = contacts.get_record(key).address
        contacts.get_record(key).delete_addr_bd()#sql/mongo |todo: change!!!
        contacts.get_record(key).delete_address()
        return f'Address "{address}" for the contact "{key}" has been successfully deleted.'
    else:
        raise CustomException('Such contact does not exist!!!')


@input_error
def delete_birthday(command_line):
    key = ' '.join(command_line).strip()
    if key in contacts.keys():
        birthday = contacts.get_record(key).birthday
        contacts.get_record(key).delete_brth_bd()#sql/mongo |todo: change!!!
        contacts.get_record(key).delete_birthday()
        return f'Date of birth {birthday} for the contact "{key}" has been successfully deleted.'
    else:
        raise CustomException('Such contact does not exist!!!')


@input_error
def delete_email(command_line):
    key = ' '.join(command_line).strip()
    if key in contacts.keys():
        email = contacts.get_record(key).email
        contacts.get_record(key).delete_eml_bd()#sql/mongo |todo: change!!!
        contacts.get_record(key).delete_email()#old_part
        return f'Email {email} for the contact "{key}" has been successfully deleted.'
    else:
        raise CustomException('Such contact does not exist!!!')


@input_error
def delete_phone(command_line):
    key, phone = prepare_value(command_line)
    if phone in contacts.get_record(key).phones_list:
        ix = contacts.get_record(key).phones_list.index(phone)
        if ix >= 0:
            contacts.get_record(key).delete_phn_bd(phone)#sql/mongo |todo: change!!!
            contacts.get_record(key).phones_list.pop(ix)
            return f'Phone number {phone} for the contact "{key}" has been successfully deleted.'
    else:
        raise CustomException('Such phone number does not exist!!!')


@input_error
def change_email(command_line):
    key, input_email = prepare_value(command_line)
    if key in contacts.keys():
        contacts.get_record(key).email = input_email
        contacts.get_record(key).change_eml_bd()#sql/mongo |todo: change!!!
        return f'Email for "{key}" has been successfully changed to {input_email}.'
    else:
        raise CustomException(
            f'Contact "{key}" does not exist or you have not specified new email!!!')


@input_error
def change_birthday(command_line):
    key, birthday = prepare_value(command_line)
    if key in contacts.keys():
        contacts.get_record(key).birthday = birthday
        contacts.get_record(key).change_brth_bd()
        return f'Date of birth for "{key}" has been successfully changed to {birthday}.'
    else:
        raise CustomException(
            f'Contact "{key}" does not exist or you have not specified new date of birth!!!')


@input_error
def change_address(command_line):
    key, address = prepare_value_3(command_line)
    if key in contacts.keys():
        contacts.get_record(key).address = address
        contacts.get_record(key).change_addr_bd()
        return f'Address for the contact "{key}" has been successfully changed to "{address}".'
    else:
        raise CustomException(
            f'Contact "{key}" does not exist!')


@input_error
def change_phone(command_line):
    phones = [command_line.pop(-1)]
    phones.insert(0, command_line.pop(-1))#list of phones
    key = ' '.join(command_line).strip()#name
    if key not in contacts.keys():
        return f'Wrong name "{key}" or you have not specified the new phone number.'
    if len(phones) != 2:
        raise CustomException(
            '''The command must be with a NAME and 2 phones you want to change 
            (Format: <change> <name> <old phone> <new phone>)''')
    if re.search('\(0\d{2}\)\d{3}-\d{2}-\d{2}', phones[1]):
        if phones[0] in contacts.get_record(key).phones_list:
            ix = contacts.get_record(key).phones_list.index(phones[0])
            if ix >= 0:
                contacts.get_record(key).phones_list[ix] = phones[1]#old part
                contacts.get_record(key).change_phn_bd(phones)
                return f'Phone number for "{key}" has been successfully changed to {phones[1]}.'
        else:
            raise CustomException(
                f'Phone number {phones[0]} does not exist!!!')
    else:
        raise CustomException(
            'Wrong phone number format. Use (0XX)XXX-XX-XX format!')


@input_error
def help_common(command_line):
    to_show = []
    try:
        file = open(
            f"{os.path.dirname(os.path.abspath(__file__))}/help.txt", 'r')
        help_lines = file.readlines()
        for i in help_lines:
            # забили последний символ переноса строки - для красивого вывода
            string = i[:len(i)-1]
            to_show.append(string)
            #print(i[:len(i)-1])
        file.close()
        msg = "The end of the help."
    except:
        msg = "File help.txt is not found."
    new_msg = "\n".join(to_show)
    help_list = HelpList(new_msg + '\n' + msg)
    return ToConsole().to_outpute(help_list)



@input_error
def show_all(command_line):
    if len(contacts.items()) > 0:
        return ToConsole().to_outpute(contacts) #str(contacts)
    else:
        return 'There are no contacts in the book.'


@input_error
def show_bd(command_line): #new fun
    mongo_con = IMongoConnact()
    return mongo_con.shw_bd()
    
#@input_error
def search_bd(command_line): #new fun
    mongo_con = IMongoConnact()
    return mongo_con.srch_bd(command_line)


COMMANDS = {
    'close': exit_func,
    'exit': exit_func,
    'good bye': exit_func,
    'save': save_func,
    'add': add_name,
    'add address': add_address,
    'add birthday': add_birthday,
    'add email': add_email,
    'add phone': add_phone,
    'remove': remove,
    'delete address': delete_address,
    'delete birthday': delete_birthday,
    'delete email': delete_email,
    'delete phone': delete_phone,
    'change email': change_email,
    'change birthday': change_birthday,
    'change address': change_address,
    'change phone': change_phone,
    'coming birthday': coming_birthday,
    "help": help_common,
    'show all': show_all,
    'search': search,
    'show bd': show_bd,
    'search bd': search_bd
}

ONE_WORD_COMMANDS = ['add', 'clean', 'close', "help",
                     'exit', 'save', 'remove', 'search']
TWO_WORDS_COMMANDS = ['add address', 'add birthday', 'add email', 'add phone',
                      'delete address', 'delete birthday', 'delete email', 'delete phone',
                      'change email', 'change birthday', 'change address', 'change phone',
                      'coming birthday', 'good bye', "add note", "find note", "change note",
                      "delete note", "tag note", 'show all', 'show bd', 'search bd']


def get_handler(command):
    return COMMANDS[command]


def main():

    print("Enter 'help' command to see all the commands available.")
    print(contacts.load_from_file(
        f"{os.path.dirname(os.path.abspath(__file__))}/contacts.bin"))

    while True:
        command_line = []
        while not command_line:
            command_line = prompt('>>> ',
                                  history=FileHistory('history'),
                                  auto_suggest=AutoSuggestFromHistory(),
                                  completer=SqlCompleter,
                                  style=style
                                  ).split()

        right_command = False

        if len(command_line) > 1 and \
           f'{command_line[0].lower()} {command_line[1].lower()}' in TWO_WORDS_COMMANDS:
            command = f'{command_line.pop(0).lower()} {command_line.pop(0).lower()}'
            right_command = True

        if not right_command:
            command = command_line.pop(0).lower()
            right_command = command in ONE_WORD_COMMANDS

        if not right_command:
            print(
                f'The "{command}" command is wrong! The allowable commands are {", ".join(ONE_WORD_COMMANDS + TWO_WORDS_COMMANDS)}.')
            continue

        handler = get_handler(command)
        print(handler(command_line))
        if handler is exit_func:
            print(contacts.save_to_file(
                f"{os.path.dirname(os.path.abspath(__file__))}/contacts.bin"))
            break


if __name__ == '__main__':
    main()

