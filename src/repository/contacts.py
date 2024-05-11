from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from src.database.models import Contact
from src.schemas import ContactSchema, ContactUpdateSchema, ContactSearchSchema


async def get_contacts(limit: int, offset: int, db: AsyncSession):
    sq = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(sq)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession):
    sq = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(sq)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactSchema, db: AsyncSession):
    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone_number=body.phone_number,
        birthday=body.birthday,
    )
    if body.data:
        contact.data = body.data
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactUpdateSchema, db: AsyncSession):
    sq = select(Contact).filter_by(id=contact_id)
    result = await db.execute(sq)
    contact = result.scalar_one_or_none()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.data = body.data
        await db.commit()
        await db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, db: AsyncSession):
    sq = select(Contact).filter_by(id=contact_id)
    result = await db.execute(sq)
    contact = result.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact



async def search_contacts(search_params: ContactSearchSchema, db: AsyncSession):
    sq = select(Contact)
    if search_params.name:
        sq = sq.filter(func.lower(Contact.first_name) ==
                       func.lower(search_params.name))
    if search_params.surname:
        sq = sq.filter(func.lower(Contact.last_name) ==
                       func.lower(search_params.surname))
    if search_params.email:
        sq = sq.filter(func.lower(Contact.email) ==
                       func.lower(search_params.email))
    contacts = await db.execute(sq)
    return contacts.scalars().all()



async def upcoming_birthdays(start_date: datetime, end_date: datetime, db: AsyncSession):
    sq = select(Contact).filter(
        func.date(Contact.birthday) >= start_date,
        func.date(Contact.birthday) <= end_date
    )
    contacts = await db.execute(sq)
    return contacts.scalars().all()
