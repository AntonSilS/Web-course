from . import db


class Contact(db.Model):

    __tablename__ = "contacts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    address = db.relationship("Address", cascade="all, delete, delete-orphan", back_populates="contact_addr")
    birthday = db.relationship("Birthday", cascade="all, delete, delete-orphan", back_populates="contact_brth")
    email = db.relationship("Email", cascade="all, delete, delete-orphan", back_populates="contact_eml")
    phone_1 = db.Column(db.String(14), nullable=True)
    phone_2 = db.Column(db.String(14), nullable=True)
    phone_3 = db.Column(db.String(14), nullable=True)

    def __repr__(self):
        return self.name

class Address(db.Model):

    __tablename__ = "address"
    id = db.Column(db.Integer, primary_key=True)
    addr = db.Column(db.String(200), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey(Contact.id, ondelete="CASCADE"))
    contact_addr = db.relationship("Contact", cascade="all, delete", back_populates="address")
    
    def __repr__(self):
        return self.addr


class Birthday(db.Model):

    __tablename__ = "birthday"
    id = db.Column(db.Integer, primary_key=True)
    brth = db.Column(db.String(10), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey(Contact.id, ondelete="CASCADE"))
    contact_brth = db.relationship("Contact", cascade="all, delete", back_populates="birthday")

    def __repr__(self):
        return self.brth


class Email(db.Model):

    __tablename__ = "email"
    id = db.Column(db.Integer, primary_key=True)
    eml = db.Column(db.String(100), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey(Contact.id, ondelete="CASCADE"))
    contact_eml = db.relationship("Contact", cascade="all, delete", back_populates="email", passive_deletes=True)

    def __repr__(self):
        return self.eml
