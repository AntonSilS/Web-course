
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey


from db import Base, engine


class Contact(Base):
    __tablename__ = "contacts_1"
    id = Column(Integer, primary_key=True)
    con_name = Column(String(100), nullable=False)
    address = relationship("Address", cascade="all, delete", back_populates="contacts_addr")
    birthday = relationship("Birthday", cascade="all, delete", back_populates="contact_brth")
    email = relationship("Email", cascade="all, delete", back_populates="contact_eml")
    phones = relationship("Phone", cascade="all, delete", back_populates="contact_p")

class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    eml = Column(String(100), nullable=False)
    contact_id = Column(Integer, ForeignKey(Contact.id, ondelete="CASCADE"))
    contact_addr = relationship("Contact", cascade="all, delete", back_populates="address")

class Birthday(Base):
    __tablename__ = "birthday"
    id = Column(Integer, primary_key=True)
    brth = Column(String(10), nullable=False)
    contact_id = Column(Integer, ForeignKey(Contact.id, ondelete="CASCADE"))
    contact_brth = relationship("Contact", cascade="all, delete", back_populates="birthday")


class Email(Base):
    __tablename__ = "email"
    id = Column(Integer, primary_key=True)
    eml = Column(String(100), nullable=False, un)
    contact_id = Column(Integer, ForeignKey(Contact.id, ondelete="CASCADE"))
    contact_eml = relationship("Contact", cascade="all, delete", back_populates="email")


class Phone(Base):
    __tablename__ = "phones"
    id = Column(Integer, primary_key=True)
    description = Column(String(14), nullable=False)
    contact_id = Column(Integer, ForeignKey(Contact.id, ondelete="CASCADE"))
    contact_p = relationship("Contact", cascade="all, delete", back_populates="phones")

if __name__ == "__main__":
    Base.metadata.create_all(engine)