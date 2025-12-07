# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from email.policy import default
from apps import db
from sqlalchemy.exc import SQLAlchemyError
from apps.exceptions.exception import InvalidUsage
import datetime as dt
from sqlalchemy.orm import relationship
from enum import Enum

class CURRENCY_TYPE(Enum):
    usd = 'usd'
    eur = 'eur'

class Product(db.Model):

    __tablename__ = 'products'

    id            = db.Column(db.Integer,      primary_key=True)
    name          = db.Column(db.String(128),  nullable=False)
    info          = db.Column(db.Text,         nullable=True)
    price         = db.Column(db.Integer,      nullable=False)
    currency      = db.Column(db.Enum(CURRENCY_TYPE), default=CURRENCY_TYPE.usd, nullable=False)

    date_created  = db.Column(db.DateTime,     default=dt.datetime.utcnow())
    date_modified = db.Column(db.DateTime,     default=db.func.current_timestamp(),
                                               onupdate=db.func.current_timestamp())
    
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    def __repr__(self):
        return f"{self.name} / ${self.price}"

    @classmethod
    def find_by_id(cls, _id: int) -> "Product":
        return cls.query.filter_by(id=_id).first() 

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return


#__MODELS__
class Mailboxes(db.Model):

    __tablename__ = 'Mailboxes'

    id = db.Column(db.Integer, primary_key=True)

    #__Mailboxes_FIELDS__
    mailbox_id = db.Column(db.String(255),  nullable=True)
    mailbox_imap = db.Column(db.String(255),  nullable=True)
    mailbox_user = db.Column(db.String(255),  nullable=True)
    mailbox_password = db.Column(db.String(255),  nullable=True)

    #__Mailboxes_FIELDS__END

    def __init__(self, **kwargs):
        super(Mailboxes, self).__init__(**kwargs)


class Mails(db.Model):

    __tablename__ = 'Mails'

    id = db.Column(db.Integer, primary_key=True)

    #__Mails_FIELDS__
    mail_id = db.Column(db.String(255),  nullable=True)
    mail_mailbox_id = db.Column(db.String(255),  nullable=True)
    mail_sender = db.Column(db.String(255),  nullable=True)
    mail_recipient = db.Column(db.String(255),  nullable=True)
    mail_subject = db.Column(db.String(255),  nullable=True)
    mail_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    mail_body_path = db.Column(db.String(255),  nullable=True)

    #__Mails_FIELDS__END

    def __init__(self, **kwargs):
        super(Mails, self).__init__(**kwargs)



#__MODELS__END
