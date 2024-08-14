# Contact Management API

This project is a REST API for managing contacts, built using FastAPI and SQLAlchemy with PostgreSQL as the database. The API allows you to perform CRUD operations on contacts, search contacts by name, surname, or email, and retrieve contacts with birthdays in the next 7 days.

## Features

- Create, read, update, and delete contacts (requires authentication).
- Search contacts by first name, last name, or email (requires authentication).
- Retrieve contacts with upcoming birthdays within the next 7 days (requires authentication).
- Secure JWT-based authentication.
- Email verification during user registration.
- Rate limiting for creating contacts.
- CORS enabled for the API.
- Upload and manage user avatars using Cloudinary.
- Password reset functionality with secure email tokens.

## Installation

### Prerequisites

- Python 3.8 or later
- PostgreSQL installed and running
- Docker (for running PostgreSQL, Redis, SMTP server, and other services)
- Cloudinary account (for managing avatars)

### Setting Up the Environment

1. **Clone the repository**: https://github.com/AndriySydor1/homework-11
2. **Set up Docker containers**:
   Use Docker Compose to set up all the necessary services (PostgreSQL, Redis, SMTP server):
   docker-compose up -d
3. **Configure the environment variables**:
   Create a .env file in the root directory with the following content:
   # Database configuration
   DATABASE_URL=postgresql://postgres:postgres@localhost/contacts_db
   # JWT Configuration
   SECRET_KEY=your_secret_key
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ALGORITHM=HS256
   # SMTP Server Configuration
   EMAIL_USER=dummy@example.com
   EMAIL_PASSWORD=dummypassword
   SMTP_SERVER=localhost
   SMTP_PORT=25
   EMAIL_FROM=dummy@example.com
   # Cloudinary Configuration
   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_api_key
   CLOUDINARY_API_SECRET=your_api_secret
   # Redis Configuration
   REDIS_URL=redis://localhost:6379
4. **Run database migrations**:
   Apply the migrations to set up the database schema:
   alembic upgrade head
5. **Start the FastAPI server**:
   Run the application with Uvicorn:
   uvicorn app.main:app --reload
   The API will be available at http://127.0.0.1:8000.

6. **Run database migrations**:
   Apply the migrations to set up the database schema:
   alembic upgrade head

7. **Start the FastAPI server**:
   uvicorn app.main:app --reload
   The API will be available at http://127.0.0.1:8000.

## Usage

### Authentication

1. **Register a New User**:
   Send a POST request to /users/register/ with the following JSON payload:
   {
   "email": "newuser@example.com",
   "password": "your_secure_password"
   }
2. **Obtain an Access Token**:
   Send a POST request to /users/token/ with the following form data:
   username=newuser@example.com&password=your_secure_password
   This will return a JWT token which you can use for authenticated requests.

### Managing Contacts

All the following operations require an Authorization header with a Bearer token obtained from the above step.

1. **Creating a Contact**:
   Send a POST request to /contacts/ with the following JSON payload:
   {
   "first_name": "John",
   "last_name": "Doe",
   "email": "john.doe@example.com",
   "phone_number": "1234567890",
   "birthday": "1980-08-09",
   "additional_info": "Friend from college"
   }
2. **Getting All Contacts**:
   Send a GET request to /contacts/.
   curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -X GET http://127.0.0.1:8000/contacts/
3. **Searching Contacts**:
   Send a GET request to /contacts/search/ with the appropriate query parameters:
   curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -X GET "http://127.0.0.1:8000/contacts/search/?first_name=John"
4. **Getting Upcoming Birthdays**:
   Send a GET request to /contacts/upcoming_birthdays/:
   curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -X GET http://127.0.0.1:8000/contacts/upcoming_birthdays/

### Password Reset

1. **Request Password Reset**:
   Send a POST request to /auth/reset-password/request/ with the email of the user:
   {
   "email": "user@example.com"
   }
2. **Reset Password**:
   After receiving the reset link, send a POST request to /auth/reset-password/ with the token and new password:
   {
   "token": "reset_token_received_via_email",
   "new_password": "new_secure_password"
   }

## License

This project is licensed under the MIT License.

## Contact

If you have any questions or feedback, feel free to reach out at AndriySydor91@gmail.com.
