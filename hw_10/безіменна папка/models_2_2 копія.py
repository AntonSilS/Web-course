
from mongoengine import EmbeddedDocument, Document
from mongoengine.fields import DateTimeField, EmbeddedDocumentField, ListField, StringField




class ContactUser(Document):
    name = StringField(max_length=200, required=True)
    address = StringField()
    birthday = StringField()
    email = StringField(max_length=100)
    #phone = ListField(EmbeddedDocumentField(PhoneUser), default=list)
    phone = ListField(StringField(max_length=14), default=list)
    meta = {'indexes': 
                [
                    {'fields': ['birthday', 'address']}
                ]
           }