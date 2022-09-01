
from flask import render_template, redirect, request
from flask import current_app as app

from .models import db, Contact, Address, Birthday, Email
from sqlalchemy import or_

from collections import defaultdict
from datetime import datetime, timedelta

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add-contact/', methods=["GET", "POST"], strict_slashes=False)
def add_contact():

    if request.method == "POST":
        name = request.form.get("username")
        contact_result = Contact.query.filter_by(name=name).first()
        
        if contact_result:
            message = f'Such contact "{name}" already exists'
            return render_template('exception.html', message=message)
        
        new_contact = Contact(name=name)
        db.session.add(new_contact)
        db.session.flush()

        user_id =  new_contact.id
        
        address = request.form.get("address")
        if address: 
            new_contact.address = [Address(addr=address, contact_id=user_id)]
        
        birthday = request.form.get("birthday")
        if birthday:
            new_contact.birthday = [Birthday(brth=birthday, contact_id=user_id)]
        
        email = request.form.get("email")
        if email:
            new_contact.email = [Email(eml=email, contact_id=user_id)]
        
        phone_1 = request.form.get("phone_1")
        if phone_1:
            new_contact.phone_1 = phone_1
        
        phone_2 = request.form.get("phone_2")
        if phone_2:
            new_contact.phone_2 = phone_2
        
        phone_3 = request.form.get("phone_3")
        if phone_3:
            new_contact.phone_3 = phone_3

        db.session.add(new_contact)
        db.session.commit()

        return redirect('/result/')

    return render_template('add-contact.html')


@app.route('/edit-contact/<id>', methods=["GET", "POST"])
def edit_contact(id):

    cont = Contact.query.filter_by(id=id).first()

    if request.args.get('id') == 'Delete':
        db.session.query(Contact).filter(Contact.id == id).delete()
        db.session.query(Email).filter(Email.contact_id == id).delete()
        db.session.query(Birthday).filter(Birthday.contact_id == id).delete()
        db.session.query(Address).filter(Address.contact_id == id).delete()
        db.session.commit()
        return redirect('/result/')

    if request.method == "POST":
        
        name = request.form.get("name")
        if name:
            cont.name = name

        address = request.form.get("address")
        if address:
            db.session.query(Address).filter(Address.contact_id == id).update({"addr": address}, synchronize_session="fetch")
            if not cont.address:
                cont.address = [Address(addr=address, contact_id=id)]

        birthday = request.form.get("birthday")
        if birthday:
            db.session.query(Birthday).filter(Birthday.contact_id == id).update({"brth": birthday}, synchronize_session="fetch")
            if not cont.birthday:
                cont.birthday = [Birthday(brth=birthday, contact_id=id)]
        email = request.form.get("email")

        if email:
            db.session.query(Email).filter(Email.contact_id == id).update({"eml": email}, synchronize_session="fetch")
            if not cont.email:
                cont.email = [Email(eml=email, contact_id=id)]

        phone_1 = request.form.get("phone_1")
        if phone_1:
            cont.phone_1 = phone_1

        phone_2 = request.form.get("phone_2")
        if phone_2:
            cont.phone_2 = phone_2

        phone_3 = request.form.get("phone_3")
        if phone_3:
            cont.phone_3 = phone_3

        db.session.add(cont)
        db.session.commit()

        contact = Contact.query.filter_by(id=id).all()

        return render_template('result.html', contacts=contact)

    return render_template('edit-contact.html', cont=cont)
    

@app.route('/result/', methods=["GET", "POST"])
def show_all():

    if request.method == "POST":

        key= request.form.get("key")
        contacts = db.session.query(Contact).\
            join(Address, isouter=True).\
            join(Birthday, isouter=True).\
            join(Email, isouter=True).\
            filter(or_(
                        Contact.name.like(f'%{key}%'),
                        Contact.phone_1.like(f'%{key}%'),
                        Contact.phone_2.like(f'%{key}%'),
                        Contact.phone_3.like(f'%{key}%'),
                        Address.addr.like(f'%{key}%'),
                        Birthday.brth.like(f'%{key}%'),
                        Email.eml.like(f'%{key}%'))).all()
        return render_template('result.html', contacts=contacts)
                                    
    contacts = Contact.query.order_by(Contact.id).all()
    return render_template('result.html', contacts=contacts)


@app.route('/birthday/', methods=["GET", "POST"])
def coming_birthday():
    range_days = 7
    birthdays_dict = defaultdict(list)
    current_date = datetime.now().date()
    timedelta_filter = timedelta(days=range_days)
    for name, birthday in [i for i in db.session.query(Contact.name, Birthday.brth).join(Birthday, isouter=True).all()]:
        if name and birthday: 
            birthday_date = datetime.strptime(birthday, '%Y-%m-%d').date()
            current_birthday = birthday_date.replace(year=current_date.year)
            if current_date <= current_birthday <= current_date + timedelta_filter:
                birthdays_dict[current_birthday].append(name)
    return render_template('birthday.html',  message= birthdays_dict)
