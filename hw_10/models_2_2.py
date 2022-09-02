
from mongoengine import EmbeddedDocument, Document
from mongoengine.fields import DateTimeField, EmbeddedDocumentField, ListField, StringField


class Address(EmbeddedDocument):
    addr = StringField()

class Birthday(EmbeddedDocument):
    brth = StringField()

class Email(EmbeddedDocument):
    eml = StringField(max_length=100)

class PhoneUser(EmbeddedDocument):
    phn = StringField(max_length=14)


class ContactUser(Document):
    name = StringField(max_length=200, required=True)
    address = EmbeddedDocumentField(Address)
    birthday = EmbeddedDocumentField(Birthday)
    email = EmbeddedDocumentField(Email)
    #phone = ListField(EmbeddedDocumentField(PhoneUser), default=list)
    phone = ListField(StringField(max_length=14), default=list)
    '''meta = {'indexes': 
                [
                    {'fields': ['birthday', 'address']}
                ]
           }'''