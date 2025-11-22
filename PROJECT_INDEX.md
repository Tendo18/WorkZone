# WorkZone - Job Portal API Project Index

## Project Overview

WorkZone is a Django REST API-based job portal that connects employers and job applicants. The project provides authentication, job posting, application management, and email notifications.

## Technology Stack

- **Backend**: Django 5.1.7 + Django REST Framework 3.15.2
- **Authentication**: JWT (JSON Web Tokens) with SimpleJWT
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Email**: SMTP (Gmail)
- **File Upload**: Pillow for image handling
- **Environment**: python-dotenv for configuration management

## Project Structure

### Core Configuration

```
api/
├── settings.py          # Main Django settings with JWT, email, and app configuration
├── urls.py              # Root URL patterns with JWT endpoints
├── wsgi.py              # WSGI application entry point
└── asgi.py              # ASGI application entry point
```

### Apps

#### 1. Users App (`users/`)

**Purpose**: User authentication, registration, and profile management

**Models**:

- `User` (extends AbstractUser): Custom user model with roles (Employer/Applicant)
  - Fields: email, phone_number, role, address, profile_image, created_at

**Views**:

- `RegisterView`: User registration with JWT token generation
- `LoginView`: User authentication with JWT token generation
- `LogoutView`: Token blacklisting for secure logout
- `UserProfileView`: Profile retrieval and update (authenticated)

**Serializers**:

- `RegisterSerializer`: Handles user registration with validation
- `UserSerializer`: User data serialization

**URLs**:

- `/api/register/` - User registration
- `/api/login/` - User login
- `/api/logout/` - User logout
- `/api/profile/` - User profile management

#### 2. Jobs App (`jobs/`)

**Purpose**: Job posting, application management, and employer functionality

**Models**:

- `Employer`: Company/employer information
  - Fields: name, user (OneToOne), description, phone, email, company, created
- `Jobs`: Job postings
  - Fields: title, employer (ForeignKey), description, location, job_Type, created
  - Job types: FullTime, Flexible, Remote, Hybrid, Internship
- `Applicants`: Job seeker profiles
  - Fields: name, user (OneToOne), jobs (ManyToMany), description, phone_no, email, status_choices, created
  - Status: Approved, Rejected, Pending
- `Application`: Job applications with resumes
  - Fields: title, applicant (ForeignKey), description, resume (FileField), created

**Views**:

- `EmployerView`: CRUD operations for employers
- `EmployerDetailView`: Individual employer management
- `JobsView`: Job posting CRUD with email notifications
- `JobsDetailView`: Individual job management
- `ApplicantsView`: Applicant profile management
- `ApplicantsDetailView`: Individual applicant management with status updates
- `ApplicationView`: Job application CRUD
- `ApplicationDetailView`: Individual application management

**Serializers**:

- `EmployerSerializer`: Employer data serialization
- `JobsSerializer`: Job data serialization
- `ApplicantsSerializer`: Applicant data serialization
- `ApplicationSerializer`: Application data with resume URL generation

**Utilities** (`utils.py`):

- `send_application_emails()`: Email notifications for new applications
- `send_status_update_email()`: Status change notifications
- `send_new_job_alert()`: New job posting alerts to users
- `get_all_users_emails()`: Retrieve user emails for notifications

**URLs**:

- `/api/employer/` - Employer management
- `/api/employer/<id>/` - Individual employer operations
- `/api/jobs/` - Job posting management
- `/api/jobs/<id>/` - Individual job operations
- `/api/applicants/` - Applicant management
- `/api/applicants/<id>/` - Individual applicant operations
- `/api/application/` - Application management
- `/api/application/<id>/` - Individual application operations

## Authentication & Security

### JWT Configuration

- Access token lifetime: 60 minutes
- Refresh token lifetime: 1 day
- Token rotation enabled
- Blacklist after rotation enabled
- Bearer token authentication

### API Endpoints

- `/api/token` - Obtain JWT token pair
- `/api/token/refresh` - Refresh access token

## Key Features

### 1. User Management

- Role-based user system (Employer/Applicant)
- JWT-based authentication
- Profile management with image upload
- Secure password validation

### 2. Job Management

- Job posting with multiple types (FullTime, Remote, etc.)
- Location-based job search
- Employer-specific job management
- Email notifications for new job postings

### 3. Application System

- Multi-job application support
- Resume upload functionality
- Application status tracking (Pending/Approved/Rejected)
- Email notifications for status changes

### 4. Email Notifications

- Application confirmation emails
- Status update notifications
- New job alert system
- Employer notifications for new applications

## Database Schema

### User Relationships

- User (1:1) → Profile
- User (1:1) → Employer
- User (1:1) → Applicants

### Job Relationships

- Employer (1:N) → Jobs
- Jobs (M:N) → Applicants
- Applicants (1:N) → Application

## Environment Configuration

The project uses environment variables for sensitive configuration:

- `SECRET_KEY`: Django secret key
- `EMAIL_HOST_USER`: Gmail username
- `EMAIL_HOST_PASSWORD`: Gmail app password

## File Structure Summary

```
WorkZone/
├── api/                 # Django project settings
├── users/              # User authentication app
├── jobs/               # Job management app
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
├── db.sqlite3         # SQLite database
└── virtual_env/       # Virtual environment
```

## API Usage Examples

### Authentication

```bash
# Register
POST /api/register/
{
  "username": "user123",
  "email": "user@example.com",
  "password": "password123",
  "confirm_password": "password123",
  "first_name": "John",
  "last_name": "Doe",
  "role": "Applicant"
}

# Login
POST /api/login/
{
  "username": "user123",
  "password": "password123"
}
```

### Job Operations

```bash
# Create job (requires authentication)
POST /api/jobs/
Authorization: Bearer <token>
{
  "title": "Software Developer",
  "description": "Python Django developer needed",
  "location": "Remote",
  "job_Type": "Remote"
}

# Get all jobs
GET /api/jobs/
```

### Application Management

```bash
# Apply for job
POST /api/application/
{
  "title": "Software Developer Application",
  "description": "I'm interested in this position",
  "resume": <file>
}
```

## Development Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Set up environment variables
3. Run migrations: `python manage.py migrate`
4. Create superuser: `python manage.py createsuperuser`
5. Run server: `python manage.py runserver`

## Production Considerations

- Configure PostgreSQL database
- Set up proper email credentials
- Configure static file serving
- Set DEBUG=False
- Use environment variables for all sensitive data
- Configure CORS if needed for frontend integration
