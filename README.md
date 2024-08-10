# Contact Management API

This project is a REST API for managing contacts, built using FastAPI and SQLAlchemy with PostgreSQL as the database. The API allows you to perform CRUD operations on contacts, search contacts by name, surname, or email, and retrieve contacts with birthdays in the next 7 days.

## Features

- Create, read, update, and delete contacts.
- Search contacts by first name, last name, or email.
- Retrieve contacts with upcoming birthdays within the next 7 days.

## Installation

### Prerequisites

- Python 3.8 or later
- PostgreSQL installed and running
- Docker (optional, for running PostgreSQL in a container)

### Setting Up the Environmen

1. **Clone the repository**: https://github.com/AndriySydor1/homework-11
2. **Set up PostgreSQL**: docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=postgres -d postgres
3. **Configure the database**: sqlalchemy.url = postgresql://postgres:postgres@localhost/contacts_db
4. **Run database migrations**: alembic upgrade head
5. **Start the FastAPI server**: uvicorn app.main:app --reload
   The API will be available at http://127.0.0.1:8000.

## Usage

1. Creating a Contact
   To create a new contact, send a POST request to /contacts/ with the following JSON payload:
   {
   "first_name": "John",
   "last_name": "Doe",
   "email": "john.doe@example.com",
   "phone_number": "1234567890",
   "birthday": "1980-08-09",
   "additional_info": "Friend from college"
   }
2. Getting All Contacts
   To retrieve all contacts, send a GET request to /contacts/.
3. Searching Contacts
   To search for contacts by first name, last name, or email, send a GET request to /contacts/search/ with the appropriate query parameters:
   curl -X GET "http://127.0.0.1:8000/contacts/search/?first_name=John"
4. Getting Upcoming Birthdays
   To retrieve contacts with birthdays in the next 7 days, send a GET request to /contacts/upcoming_birthdays/.

## License

This project is licensed under the MIT License.

## Contact

If you have any questions or feedback, feel free to reach out at AndriySydor91@gmail.com
