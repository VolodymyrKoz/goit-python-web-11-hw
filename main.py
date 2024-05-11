from fastapi import FastAPI, Query
from starlette.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta

from src.routes import contacts
from src.models import Contact

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contacts.router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "Contacts API"}


@app.get("/api/search/")
def search_contacts(
    name: str = Query(None),
    surname: str = Query(None),
    email: str = Query(None)
):
    pass


@app.get("/api/birthdays/")
def upcoming_birthdays():
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=7)

    pass
