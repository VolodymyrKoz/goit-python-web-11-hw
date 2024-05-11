from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base
from sqlalchemy import func
from datetime import datetime, timedelta

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(150))
    last_name = Column(String(150), unique=True, index=True)
    email = Column(String(150))
    phone_number = Column(String(30))
    birthday = Column(String(30))
    data = Column(Boolean, default=False, nullable=True)

    @classmethod
    def search(cls, session, name=None, surname=None, email=None):
        query = session.query(cls)
        if name:
            query = query.filter(func.lower(
                cls.first_name) == func.lower(name))
        if surname:
            query = query.filter(func.lower(cls.last_name)
                                 == func.lower(surname))
        if email:
            query = query.filter(func.lower(cls.email) == func.lower(email))
        return query.all()

    @classmethod
    def upcoming_birthdays(cls, session):
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=7)
        return session.query(cls).filter(
            func.date(cls.birthday) >= start_date,
            func.date(cls.birthday) <= end_date
        ).all()
