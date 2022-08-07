
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey


Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts_1"
    id = Column(Integer, primary_key=True)
    con_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True)
    phones = relationship("Phone", cascade="all, delete", back_populates="contacts_p")

class Phone(Base):
    __tablename__ = "phones"
    id = Column(Integer, primary_key=True)
    description = Column(String(14), nullable=False)
    contact_id = Column(Integer, ForeignKey(Contact.id, ondelete="CASCADE"))
    contacts_p = relationship("Contact", cascade="all, delete", back_populates="phones")