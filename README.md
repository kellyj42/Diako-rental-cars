# Diako Rental Cars - Complete Documentation

## Project Overview

**Daiko Rental Cars** is a comprehensive, full-stack web application for managing vehicle rentals. It provides a complete platform where customers can browse available cars, make bookings, and manage their rental history, while administrators can manage inventory, pricing, and bookings.

**Chief Developer:** Kelly Jnambale  
**Built With:** Django (Python Backend), Tailwind CSS (Frontend)  
**Status:** Production Ready (Deployed on Railway)

---

## Table of Contents

1. [Architecture & System Design](#architecture--system-design)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Database Schema & Models](#database-schema--models)
5. [Installation & Setup](#installation--setup)
6. [Development Process](#development-process)
7. [Key Features](#key-features)
8. [Deployment](#deployment)
9. [Configuration](#configuration)
10. [API Endpoints](#api-endpoints)

---

## Architecture & System Design

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE (CLIENT)                  │
│              HTML/CSS (Tailwind CSS) + JavaScript            │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP REQUEST/RESPONSE
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                   DJANGO WEB APPLICATION                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    URL ROUTING                        │   │
│  │  (Diakorentalcars/urls.py - Main URL Configuration) │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              VIEWS & BUSINESS LOGIC                  │   │
│  │  - Car Management, Booking System, Authentication   │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                  FORMS & VALIDATION                  │   │
│  │  - Input validation, Security checks, CSRF          │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │            MODELS & DATA MANAGEMENT                  │   │
│  │  - Car, Booking, User, Profile, Category Models     │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────────┘
                       │ READ/WRITE
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                   SQLITE3 DATABASE                            │
│  - Production: PostgreSQL (Railway)                           │
│  - Development: SQLite3 (db.sqlite3)                          │
└──────────────────────────────────────────────────────────────┘

ADDITIONAL SERVICES:
├─ SendGrid Email Service (Email Verification, Notifications)
├─ WhiteNoise (Static Files Management)
└─ Gunicorn (Production WSGI Server)
```

### System Components

The system is organized into **6 main Django applications**, each handling a specific domain:

#### 1. **Home App** (`home/`)

- Landing page and public-facing content
- Main entry point for users
- Car listing and browsing functionality

#### 2. **User Authentication App** (`userAuth/`)

- User registration (signup)
- Email verification system
- Login/Logout functionality
- Password management
- User profile management
- Authentication tokens and verification
- Phone number validation

#### 3. **Cars App** (`cars/`)

- Car inventory management
- Car categories (SUV, Sedan, Budget, etc.)
- Car specifications (transmission, fuel type, seats, etc.)
- Car features (GPS, Bluetooth, AC, Sunroof, etc.)
- Car pricing (price per day)
- Car images and thumbnails
- Admin CRUD operations for cars

#### 4. **Bookings App** (`bookings/`)

- Booking form and processing
- Booking details management
- Pick-up and drop-off locations
- Date/time selection
- Booking status tracking (Draft, Confirmed, Cancelled, Expired)
- Additional notes for special requests
- User booking history

#### 5. **Dashboard App** (`dashboard/`)

- Admin dashboard
- Admin authentication (decorators)
- Admin-only views and management
- Booking management interface
- Statistics and analytics

#### 6. **About App** (`about/`)

- Static content pages
- Company information
- Contact and legal pages

### Theme System

- **Theme App** (`theme/`)
  - Tailwind CSS integration
  - Custom CSS compilation
  - Static file management

---

## Technology Stack

### Backend

- **Framework:** Django 6.0.1 - Modern Python web framework with built-in ORM
- **Database (Dev):** SQLite3 - File-based database for local development
- **Database (Prod):** PostgreSQL - Robust relational database on Railway
- **Python Version:** 3.8+

### Frontend

- **CSS Framework:** Tailwind CSS 3.4.0 - Utility-first CSS for rapid UI development
- **Template Engine:** Django Templates - Server-side rendering
- **JavaScript:** Vanilla JS + Django Template language

### Security & Deployment

- **Web Server (Dev):** Django Development Server
- **Web Server (Prod):** Gunicorn 25.0.3 - WSGI HTTP server
- **Static Files:** WhiteNoise 6.11.0 - Zero-config static file handling
- **HTTPS:** Enforced via CSRF_TRUSTED_ORIGINS and SECURE_PROXY_SSL_HEADER
- **Session Security:** Secure cookies with SameSite=Lax

### External Services

- **Email:** SendGrid 6.12.5 - Email verification and notifications
- **Image Processing:** Pillow 12.1.0 - Image handling and resizing

### Database & ORM

- **ORM:** Django ORM - Object-relational mapping
- **Database URL:** dj-database-url 3.1.0 - Environment-based database configuration

### Development Tools

- **Hot Reload:** django-browser-reload 1.21.0 - Auto-refresh during development
- **Security:** cryptography 46.0.5 - Cryptographic recipes

### Dependencies Summary

```
Core: asgiref, Django, sqlparse, tzdata
Database: dj-database-url, psycopg2-binary
Frontend: MarkupSafe, Werkzeug
Deployment: gunicorn, whitenoise
Email: sendgrid, python-http-client
CSS: django-tailwind, pytailwindcss, tailwindcss
Development: django-browser-reload
Images: Pillow
Security: cryptography, pycparser
```

---

## Project Structure

```
Diako-rental-cars-main/
│
├── Diakorentalcars/              # Main Django project settings
│   ├── __init__.py
│   ├── settings.py               # Django configuration (databases, apps, middleware, etc.)
│   ├── urls.py                   # Main URL router for entire application
│   ├── asgi.py                   # ASGI config for async servers
│   ├── wsgi.py                   # WSGI config for gunicorn deployment
│   └── __pycache__/
│
├── home/                         # Home/Landing page application
│   ├── models.py                 # Data models (if any)
│   ├── views.py                  # View logic for home pages
│   ├── urls.py                   # URL patterns for home app
│   ├── forms.py                  # Forms for home app
│   ├── admin.py                  # Django admin configuration
│   ├── apps.py                   # App configuration
│   ├── tests.py                  # Unit tests
│   ├── templates/
│   │   └── home/                 # HTML templates for home app
│   │       ├── index.html
│   │       ├── about.html
│   │       └── ...
│   └── migrations/               # Database migration files
│
├── userAuth/                     # User authentication application
│   ├── models.py                 # User Profile model
│   ├── views.py                  # Login, Signup, Email Verification, Logout
│   ├── urls.py                   # Authentication URL patterns
│   ├── forms.py                  # SignUpForm, UserManageForm with validation
│   ├── signals.py                # Django signals (auto-create Profile on User creation)
│   ├── tokens.py                 # Email verification token generation
│   ├── utils.py                  # Email sending and utility functions
│   ├── admin.py                  # User admin configuration
│   ├── apps.py                   # App configuration
│   ├── tests.py                  # Unit tests
│   ├── templates/
│   │   └── userAuth/             # Login, Signup, Email Verification templates
│   │       ├── login.html
│   │       ├── signUp.html
│   │       ├── emailVerification.html
│   │       └── ...
│   └── migrations/               # Database migrations for Profile model
│
├── cars/                         # Car inventory application
│   ├── models.py                 # Car, CarCategory models with detailed specs
│   ├── views.py                  # Car listing, detail, CRUD for admin
│   ├── urls.py                   # Car URL patterns
│   ├── forms.py                  # CarForm for creating/editing cars
│   ├── admin.py                  # Car admin configuration
│   ├── apps.py                   # App configuration
│   ├── tests.py                  # Unit tests
│   ├── templates/
│   │   └── cars/                 # Car listing, detail, management templates
│   │       ├── cars.html         # All cars listing page
│   │       ├── car_detail.html   # Individual car detail page
│   │       ├── car_form.html     # Admin form for creating/editing cars
│   │       ├── car_manage_list.html
│   │       └── ...
│   ├── migrations/               # Database migrations for Car models
│   │   ├── 0001_initial.py
│   │   ├── 0002_car_price_per_day.py
│   │   ├── 0003_remove_car_price_per_day.py
│   │   ├── 0004_car_price_per_day.py
│   │   ├── 0005_remove_car_main_image.py
│   │   └── ...
│   └── main/                     # Additional module
│
├── bookings/                     # Booking system application
│   ├── models.py                 # Booking model with status tracking
│   ├── views.py                  # Booking form, details, history, admin views
│   ├── urls.py                   # Booking URL patterns
│   ├── forms.py                  # BookingForm with comprehensive validation
│   ├── context_processors.py     # Template context data
│   ├── admin.py                  # Booking admin configuration
│   ├── apps.py                   # App configuration
│   ├── tests.py                  # Unit tests
│   ├── templates/
│   │   └── bookings/             # Booking form, confirmation templates
│   │       ├── bookingform.html
│   │       ├── booking_details.html
│   │       └── ...
│   └── migrations/               # Database migrations for Booking model
│
├── dashboard/                    # Admin dashboard application
│   ├── models.py                 # Dashboard data models
│   ├── views.py                  # Dashboard home, admin views
│   ├── urls.py                   # Dashboard URL patterns
│   ├── decorators.py             # @admin_required decorator for protected views
│   ├── admin.py                  # Dashboard admin configuration
│   ├── apps.py                   # App configuration
│   ├── tests.py                  # Unit tests
│   ├── templates/
│   │   └── dashboard/            # Admin dashboard templates
│   │       ├── home.html
│   │       ├── bookings.html
│   │       └── ...
│   └── migrations/               # Database migrations
│
├── about/                        # About/Company info application
│   ├── models.py                 # Static content models
│   ├── views.py                  # About page views
│   ├── urls.py                   # About URL patterns
│   ├── admin.py                  # About admin configuration
│   ├── templates/
│   │   └── about/                # About, contact templates
│   │       └── about.html
│   └── migrations/               # Database migrations
│
├── theme/                        # Tailwind CSS theme configuration
│   ├── static/
│   │   └── css/
│   │       ├── style.css         # Custom CSS
│   │       └── tailwind.css      # Compiled Tailwind CSS
│   └── static_src/
│       ├── package.json          # Node dependencies for Tailwind
│       ├── postcss.config.js     # PostCSS configuration
│       └── src/
│           └── input.css         # Source Tailwind configuration
│
├── templates/                    # Global templates
│   ├── base.html                 # Base template (extends to all pages)
│   └── includes/
│       ├── nav.html              # Navigation bar
│       ├── footer.html           # Footer
│       └── back_button.html      # Back button component
│
├── static/                       # Frontend static files (development)
│   ├── home/
│   │   ├── css/                  # Home-specific CSS
│   │   ├── images/               # Home-specific images
│   │   └── js/                   # Home-specific JavaScript
│   └── ...
│
├── media/                        # User-uploaded files
│   └── cars/
│       └── thumbnails/           # Car thumbnail images
│
├── staticfiles/                  # Production static files (collected)
│   ├── admin/
│   ├── css/
│   ├── django-browser-reload/
│   ├── home/
│   └── ...
│
├── env/                          # Python virtual environment
│   ├── Scripts/                  # Executable scripts
│   │   ├── python.exe
│   │   ├── pip.exe
│   │   └── activate.bat
│   ├── Lib/
│   │   └── site-packages/        # Installed packages
│   └── pyvenv.cfg
│
├── db.sqlite3                    # SQLite database (development)
├── manage.py                     # Django management command
├── package.json                  # Node.js dependencies
├── Procfile                      # Heroku/Railway deployment configuration
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## Database Schema & Models

### Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         DATABASE SCHEMA                              │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────────────┐
│    User (Django Auth)    │
├──────────────────────────┤
│ id (PK)                  │
│ username (Email)         │
│ email                    │
│ first_name               │
│ last_name                │
│ password (Hashed)        │
│ is_staff                 │
│ is_active                │
│ created_at               │
└──────────────────┬───────┘
                   │ (1:1)
                   │
┌──────────────────▼──────────────────┐
│       Profile (Custom Model)         │
├──────────────────────────────────────┤
│ id (PK)                              │
│ user_id (FK to User, OneToOne)       │
│ is_verified (Boolean)                │
│ phone_number                         │
│ last_seen_bookings_at (DateTime)     │
└──────────────────────────────────────┘


┌──────────────────────────┐
│    CarCategory           │
├──────────────────────────┤
│ id (PK)                  │
│ name                     │
│ slug (Unique)            │
│ icon                     │
│ description              │
└──────────────────┬───────┘
                   │ (1:Many)
                   │
┌──────────────────▼──────────────────┐
│          Car                         │
├──────────────────────────────────────┤
│ id (PK)                              │
│ category_id (FK to CarCategory)      │
│ name                                 │
│ model                                │
│ year                                 │
│ price_per_day (Decimal)              │
│ transmission (Choice: Auto/Manual)   │
│ fuel_type (Choice: Petrol/Diesel)    │
│ drive_type (2WD/4WD)                 │
│ seats                                │
│ doors                                │
│ engine_capacity                      │
│ color                                │
│ air_conditioning (Boolean)           │
│ bluetooth (Boolean)                  │
│ gps (Boolean)                        │
│ child_seat (Boolean)                 │
│ sunroof (Boolean)                    │
│ features (Text)                      │
│ thumbnail (ImageField)               │
│ created_at (DateTime)                │
│ updated_at (DateTime)                │
└──────────────────┬───────────────────┘
                   │ (1:Many)
                   │
┌──────────────────▼──────────────────┐
│        Booking                       │
├──────────────────────────────────────┤
│ id (PK)                              │
│ user_id (FK to User)                 │
│ car_id (FK to Car)                   │
│ pick_up_location                     │
│ drop_off_location                    │
│ pick_up_date                         │
│ pick_up_time                         │
│ drop_off_date                        │
│ drop_off_time                        │
│ additional_notes (TextField)         │
│ status (Draft/Confirmed/Cancel/Exp)  │
│ created_at (DateTime)                │
│ updated_at (DateTime)                │
└──────────────────────────────────────┘
```

### Complete Model Details

#### **User Model (Django Built-in)**

- Managed by Django's authentication system
- Extended with custom Profile model

#### **Profile Model**

```python
class Profile(models.Model):
    user = OneToOneField(User)  # One user = One profile
    is_verified = Boolean       # Email verification status
    phone_number = String(20)   # Customer phone number
    last_seen_bookings_at = DateTime  # Track user activity
```

**Purpose:** Extend Django User with application-specific fields

#### **CarCategory Model**

```python
class CarCategory(models.Model):
    name = String(100)          # e.g., "SUV", "Sedan", "Budget"
    slug = Slug(unique)         # URL-friendly identifier
    icon = String(50)           # FontAwesome icon class
    description = Text          # Category description
```

**Purpose:** Categorize cars (SUV, Sedan, Truck, Budget, Premium, etc.)

#### **Car Model**

```python
class Car(models.Model):
    # Foreign Keys & Relations
    category = ForeignKey(CarCategory)  # Which category does this car belong to?

    # Basic Information
    name = String(200)          # e.g., "Toyota Corolla 2023"
    model = String(100)         # e.g., "Corolla"
    year = PositiveInteger      # Manufacturing year
    price_per_day = Decimal     # Rental price in USD

    # Specifications
    seats = PositiveInteger     # Default: 4
    doors = PositiveInteger     # Default: 4
    transmission = Choice       # Automatic/Manual/Semi-Automatic
    fuel_type = Choice          # Petrol/Diesel/Hybrid/Electric
    drive_type = Choice         # 2WD/4WD
    engine_capacity = String    # e.g., "1.8L"
    color = String

    # Features (Boolean flags)
    air_conditioning = Boolean  # Default: True
    bluetooth = Boolean         # Default: True
    gps = Boolean              # Default: False
    child_seat = Boolean       # Default: False
    sunroof = Boolean          # Default: False
    features = Text            # Additional comma-separated features

    # Media
    thumbnail = ImageField     # Car image (upload_to: 'cars/thumbnails/')
    created_at = DateTime      # When added to inventory
    updated_at = DateTime      # Last update time
```

**Purpose:** Store car inventory with specifications and features

#### **Booking Model**

```python
class Booking(models.Model):
    # Relations
    user = ForeignKey(User)     # Which user made this booking?
    car = ForeignKey(Car)       # Which car is being rented?

    # Location Details
    pick_up_location = String(255)   # Where to pick up car
    drop_off_location = String(255)  # Where to return car

    # Date/Time Details
    pick_up_date = Date
    pick_up_time = Time
    drop_off_date = Date
    drop_off_time = Time

    # Additional Info
    additional_notes = Text     # Special requests/notes
    status = Choice             # Draft/Confirmed/Cancelled/Expired

    # Tracking
    created_at = DateTime       # When booking was created
    updated_at = DateTime       # When booking was last updated
```

**Purpose:** Track customer car rental bookings and their status

---

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Node.js (for Tailwind CSS compilation)
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Diako-rental-cars-main
```

### Step 2: Create and Activate Virtual Environment

**Windows (PowerShell):**

```powershell
# Create virtual environment
python -m venv env

# Activate virtual environment
.\env\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

```cmd
python -m venv env
.\env\Scripts\activate.bat
```

**macOS/Linux:**

```bash
python3 -m venv env
source env/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Key packages installed:**

- `Django==6.0.1` - Web framework
- `psycopg2-binary==2.9.11` - PostgreSQL adapter
- `Pillow==12.1.0` - Image handling
- `sendgrid==6.12.5` - Email service
- `gunicorn==25.0.3` - Production WSGI server
- `whitenoise==6.11.0` - Static file handling
- `django-tailwind==4.4.2` - Tailwind CSS integration
- `django-browser-reload==1.21.0` - Hot reload for development

### Step 4: Install Node.js Dependencies (for Tailwind)

```bash
npm install
```

### Step 5: Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (for development, SQLite is default)
# DATABASE_URL=sqlite:///db.sqlite3

# Email Configuration (SendGrid)
SENDGRID_API_KEY=your-sendgrid-api-key-here
SENDGRID_FROM_EMAIL=noreply@diakorentalcars.com

# Railway Production Settings (when deployed)
# DATABASE_URL=postgresql://user:password@host:port/dbname
# SECURE_SSL_REDIRECT=True
```

### Step 6: Run Database Migrations

```bash
# Apply all pending migrations
python manage.py migrate

# Run migrations from specific app (if needed)
python manage.py migrate cars
python manage.py migrate userAuth
python manage.py migrate bookings
```

### Step 7: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
# Follow prompts to enter:
# - Username (email recommended)
# - Email
# - First Name
# - Last Name
# - Password
```

### Step 8: Compile Tailwind CSS

```bash
# Build CSS from Tailwind sources
npm run build:css

# Or with Django command
python manage.py tailwind build
```

### Step 9: Collect Static Files (Optional for development)

```bash
python manage.py collectstatic --noinput
```

### Step 10: Run Development Server

```bash
# Start Django development server (http://localhost:8000)
python manage.py runserver

# Or specify port
python manage.py runserver 0.0.0.0:8000
```

Access the application:

- **Frontend:** http://localhost:8000
- **Admin Panel:** http://localhost:8000/admin
- **Dashboard:** http://localhost:8000/dashboard (admin only)

---

## Development Process

### Initial Setup Phase

1. **Created Django Project Structure**
   - Initialized Django project: `Diakorentalcars`
   - Configured base settings, database, middleware, and apps

2. **Core User Authentication System**
   - Built custom user registration with email verification
   - Implemented login/logout with secure session handling
   - Extended User model with custom Profile model
   - Added phone number validation
   - Integrated SendGrid for email verification

3. **Car Inventory Management**
   - Created Car and CarCategory models
   - Defined car specifications (transmission, fuel, drive type)
   - Added feature flags (GPS, Bluetooth, AC, Sunroof, Child Seat)
   - Implemented pricing per day
   - Added car image/thumbnail support

4. **Booking System**
   - Created Booking model with status tracking
   - Implemented booking form with location and date/time validation
   - Added session-based car selection
   - Built booking confirmation flow
   - Integrated security validation (XSS/HTML injection prevention)

5. **Dashboard & Admin**
   - Built admin dashboard with protected views
   - Created @admin_required decorator for authentication
   - Implemented car CRUD operations
   - Added booking management interface

### Database Migration History

```
Migrations Timeline:

Initial Setup (Django creates default tables):
  - auth_user, auth_group, auth_permission
  - django_content_type, django_session

userAuth App:
  0001_initial.py       → Created: Profile model
  0002_profile_phone    → Added: phone_number field

cars App:
  0001_initial.py       → Created: Car, CarCategory models
  0002_car_price_per_day → Added: price_per_day field
  0003_remove_car_main  → Removed: main_image field
  0004_car_price_per_day → Re-added: price_per_day (after removal)
  0005_remove_car_main  → Removed: main_image field (final cleanup)

bookings App:
  0001_initial.py       → Created: Booking model with all fields
```

### Frontend Development

- **Base Template:** Created `base.html` with navigation and footer
- **Responsive Design:** Used Tailwind CSS for mobile-first approach
- **Reusable Components:** Built includes (nav.html, footer.html, back_button.html)
- **Template Structure:** Organized app-specific templates in subdirectories

### Security Implementation

- **CSRF Protection:** Enabled CSRF tokens on all forms
- **Password Security:** Minimum 8 characters, password matching validation
- **Email Validation:** Regex pattern validation in signup form
- **Input Sanitization:** HTML tag blocking and script pattern detection in BookingForm
- **Location Validation:** Regex pattern matching for location fields
- **SQL Injection:** Protected via Django ORM parameterized queries
- **Session Security:** Secure and HttpOnly cookies
- **HTTPS Enforcement:** Configured for production deployment

### Configuration & Optimization

1. **Static Files:**
   - WhiteNoise for zero-configuration static file serving
   - Tailwind CSS compilation pipeline
   - Separate `static_src/` for source files

2. **Performance:**
   - Database query optimization (select_related, prefetch_related)
   - Static file compression via WhiteNoise
   - Image thumbnail optimization via Pillow

3. **Email Integration:**
   - SendGrid SMTP configuration
   - Automated email verification on signup
   - Custom email utilities for sending verification links

---

## Key Features

### 1. User Management

- **Registration:** Multi-field signup with phone number support
- **Email Verification:** Token-based email verification system
- **Login/Logout:** Session-based authentication with "Remember Me"
- **Profile:** User profiles with phone number and verification status
- **Admin Support:** Staff member identification for dashboard access

### 2. Car Catalog

- **Categorization:** Organize cars by type (SUV, Sedan, Budget, etc.)
- **Specifications:** Detailed car info (transmission, fuel, drive type, capacity)
- **Features:** Boolean toggles for amenities (GPS, Bluetooth, AC, Sunroof, Child Seat)
- **Pricing:** Daily rental rates per vehicle
- **Images:** Thumbnail gallery for each car
- **Search/Filter:** Browse by category and trip type

### 3. Booking System

- **Session-Based Selection:** Select car, persist via session
- **Booking Form:** Comprehensive form with location, date/time, notes
- **Date Validation:** Ensure valid date ranges
- **Location Validation:** Prevent invalid location entries
- **Status Tracking:** Draft → Confirmed → Completed/Cancelled
- **Booking History:** Users can view their past and current bookings

### 4. Admin Dashboard

- **Car Management:** Full CRUD operations for vehicle inventory
- **Booking Management:** View and manage all customer bookings
- **User Management:** Monitor registered users and their profiles
- **Protected Views:** Admin-only access with @admin_required decorator
- **Statistics:** Track bookings and revenue data

### 5. Security Features

- **Email Verification:** Required for account activation
- **CSRF Protection:** Tokens on all POST forms
- **Input Validation:** Multi-layer form validation
- **XSS Prevention:** HTML tag and script detection in user inputs
- **Secure Session:** Secure and HttpOnly cookies
- **SSL/TLS:** HTTPS enforcement in production

---

## Deployment

### Production Environment: Railway

**Deployment Configuration:**

```plaintext
Procfile (Railway Process):
$ web: gunicorn Diakorentalcars.wsgi:application
```

**Steps to Deploy to Railway:**

1. **Connect Repository:**
   - Push code to GitHub
   - Connect GitHub repo to Railway project

2. **Environment Variables (Railway Dashboard):**

   ```
   SECRET_KEY=<production-secret-key>
   DEBUG=False
   DATABASE_URL=postgresql://<generated-by-railway>
   SENDGRID_API_KEY=<your-sendgrid-key>
   ALLOWED_HOSTS=diakorentalcars-production.up.railway.app
   ```

3. **Database Setup:**
   - Railway auto-provisions PostgreSQL
   - Run migrations: `python manage.py migrate` (in Railway console)

4. **Static Files:**
   - WhiteNoise handles collection automatically
   - Built CSS assets must be included in deployment

5. **Custom Domain (Optional):**
   - Configure domain in Railway settings
   - Update ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS

**Production Settings Applied:**

- `DEBUG = False` (hide error details)
- `CSRF_TRUSTED_ORIGINS` includes production domain
- `SECURE_PROXY_SSL_HEADER` for HTTPS detection
- `CSRF_COOKIE_SECURE = True` (HTTPS only)
- `SESSION_COOKIE_SECURE = True` (HTTPS only)
- PostgreSQL database instead of SQLite

**Live URL:**
https://diakorentalcars-production.up.railway.app

---

## Configuration

### Django Settings Hierarchy

**File:** `Diakorentalcars/settings.py`

#### Application Installation

```python
INSTALLED_APPS = [
    # Django Built-ins
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'tailwind',
    'theme',
    'django_browser_reload',  # (development only)

    # Custom Apps
    'home',
    'userAuth',
    'cars',
    'bookings',
    'about',
    'dashboard',
]
```

#### Middleware Pipeline

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',        # Static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',         # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

#### Database Configuration

```python
# Development: SQLite (file-based)
# Production: PostgreSQL (via dj-database-url)

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600,
    )
}
```

#### Security Settings

```python
SECRET_KEY = os.getenv("SECRET_KEY", "default-dev-key")
DEBUG = True  # Development only
ALLOWED_HOSTS = ["*"]  # Allow all hosts (restrict in production)

# CSRF Protection
CSRF_TRUSTED_ORIGINS = [
    "https://diakorentalcars-production.up.railway.app",
]

# Cookie Security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"

# SSL/TLS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

#### Tailwind CSS Configuration

```python
TAILWIND_APP_NAME = "theme"
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"  # Windows
# or /usr/bin/npm  # Unix
```

---

## API Endpoints

### Authentication Routes

```
POST   /auth/signup/              → Create new user account
POST   /auth/login/               → User login
POST   /auth/logout/              → User logout
GET    /auth/verify/<token>/      → Email verification
POST   /auth/resend-verification/ → Resend verification email
POST   /auth/reset-password/      → Password reset
```

### Car Routes

```
GET    /cars/                     → List all cars with filters
GET    /cars/<id>/                → Car detail page
POST   /cars/select/              → Select car (stores in session)

# Admin Only
GET    /cars/manage/              → Car inventory management
GET    /cars/manage/create/       → Car creation form
POST   /cars/manage/create/       → Submit new car
GET    /cars/manage/<id>/edit/    → Edit car form
POST   /cars/manage/<id>/edit/    → Submit car update
GET    /cars/manage/<id>/delete/  → Delete confirmation
POST   /cars/manage/<id>/delete/  → Confirm deletion
```

### Booking Routes

```
GET    /bookings/form/            → Booking form page
POST   /bookings/form/            → Create booking (draft status)
GET    /bookings/<id>/            → Booking details/confirmation
POST   /bookings/<id>/confirm/    → Confirm booking (draft → confirmed)
POST   /bookings/<id>/cancel/     → Cancel booking
GET    /bookings/my-bookings/     → User's booking history

# Admin Only
GET    /bookings/manage/          → All bookings management
POST   /bookings/<id>/approve/    → Approve booking
POST   /bookings/<id>/reject/     → Reject booking
```

### Dashboard Routes (Admin Only)

```
GET    /dashboard/                → Dashboard home
GET    /dashboard/bookings/       → Booking management
GET    /dashboard/cars/           → Car inventory
GET    /dashboard/users/          → User management
```

### Global Routes

```
GET    /                          → Home page
GET    /admin/                    → Django admin interface
GET    /__reload__/              → Browser reload (development)
```

---

## Development Commands

### Migration Commands

```bash
# Create migrations for changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations

# Reverse migrations
python manage.py migrate <app_name> <migration_number>
```

### Management Commands

```bash
# Create superuser (admin account)
python manage.py createsuperuser

# Access Django shell
python manage.py shell

# Load data from fixtures
python manage.py loaddata <fixture_name>

# Run tests
python manage.py test
```

### CSS Commands

```bash
# Build Tailwind CSS
npm run build:css

# Watch Tailwind CSS changes (development)
python manage.py tailwind start
```

### Deployment Commands

```bash
# Collect static files (before production)
python manage.py collectstatic

# Run production server (local test)
gunicorn Diakorentalcars.wsgi:application --bind 0.0.0.0:8000
```

---

## Testing & Quality Assurance

### Testing Structure

Each app includes `tests.py` for unit testing. To run tests:

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test cars
python manage.py test bookings
python manage.py test userAuth

# Run with verbose output
python manage.py test --verbosity=2
```

### Manual Testing Checklist

- [ ] User signup with email verification
- [ ] User login with secure authentication
- [ ] Car catalog browsing and filtering
- [ ] Car selection and session persistence
- [ ] Booking form with all validations
- [ ] Booking confirmation and status tracking
- [ ] Admin car CRUD operations
- [ ] Admin booking management
- [ ] Responsive design on mobile/tablet/desktop
- [ ] Image uploads and display
- [ ] Email notifications
- [ ] Admin-only view protection

---

## Troubleshooting

### Common Issues & Solutions

**Issue: Static files not loading**

```bash
# Solution: Collect static files
python manage.py collectstatic --noinput

# Clear cache and rebuild
rm -rf staticfiles/
python manage.py collectstatic --noinput
```

**Issue: Database migrations fail**

```bash
# Check migration status
python manage.py showmigrations

# Fake migrations if tables already exist
python manage.py migrate --fake-initial
```

**Issue: Email verification not sending**

- Check SENDGRID_API_KEY in environment variables
- Verify SENDGRID_FROM_EMAIL is set correctly
- Check SendGrid account for API key validity

**Issue: CSS not compiling**

```bash
# Ensure Node.js and npm are installed
node --version
npm --version

# Rebuild Tailwind
npm run build:css
```

**Issue: Import errors in development**

```bash
# Ensure virtual environment is activated
.\env\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

---

## CRITICAL SYSTEM FLAWS & VULNERABILITIES ⚠️

This section documents all known issues, vulnerabilities, and architectural flaws that could lead to crashes, security breaches, data corruption, or system failures. **Must be addressed before production.**

### 🔴 CRITICAL SEVERITY

#### 1. **Authorization Bypass - View Booking Details**

**File:** `bookings/views.py` Line: ~75  
**Issue:** `booking_details_view()` has NO ownership check. Any user can view ANY booking ID.

```python
def booking_details_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)  # ❌ No owner check!
```

**Impact:** Data breach - users see others' rental details  
**Fix:** Add `user=request.user` filter

#### 2. **Authorization Bypass - Confirm Booking**

**File:** `bookings/views.py` Line: ~101  
**Issue:** Any authenticated user can confirm ANY draft booking (ownership not verified).

```python
def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.user = request.user  # ❌ Silently overwrites!
```

**Impact:** Users can steal/confirm others' bookings

#### 3. **No Auth on Car Selection**

**File:** `bookings/views.py` Line: ~17  
**Issue:** `selectedVehicle()` missing `@login_required` and car_id validation.
**Impact:** Session injection, invalid booking flow

#### 4. **No Auth on Draft Save**

**File:** `bookings/views.py` Line: ~98  
**Issue:** `save_booking_draft()` missing `@login_required`.
**Impact:** Unauthenticated session manipulation

#### 5. **DEBUG = True (Hardcoded)**

**File:** `Diakorentalcars/settings.py` Line: 31  
**Issue:** Exposes stack traces in production.
**Impact:** Information disclosure

#### 6. **ALLOWED_HOSTS = ["*"]**

**File:** `Diakorentalcars/settings.py` Line: 33  
**Issue:** Accepts ANY hostname.
**Impact:** Host header injection, cache poisoning

#### 7. **Hardcoded Secret Key**

**File:** `Diakorentalcars/settings.py` Line: 25  
**Issue:** Default SECRET_KEY exposed in source code.
**Impact:** Session hijacking, CSRF bypass

#### 8. **Car DELETE Cascades to Booking**

**File:** `bookings/models.py` Line: ~20  
**Issue:** `on_delete=models.CASCADE` deletes all bookings when car deleted.
**Impact:** Data loss, no audit trail

#### 9. **Booking User Field Nullable**

**File:** `bookings/models.py` Line: ~14  
**Issue:** `user=ForeignKey(..., null=True, blank=True)` allows orphaned bookings.
**Impact:** Data integrity violation

#### 10. **No Time Validation (Same-Day)**

**File:** `bookings/forms.py` Line: ~87  
**Issue:** Doesn't validate time logic for same-day bookings.
**Impact:** drop_time can be BEFORE pick_time

#### 11. **Profile Creation Fails Silently**

**File:** `userAuth/signals.py` Line: ~11  
**Issue:** No error handling; crashes later when accessing user.profile.
**Impact:** AttributeError in login/verification

### 🟠 HIGH SEVERITY

#### 12. **N+1 Query: Car List**

**File:** `cars/views.py` Line: ~10

```python
cars = Car.objects.all()  # Loads ALL
categories = CarCategory.objects.all()
rates = CarRate.objects.all()  # Could be 1000s
```

**Impact:** Memory crash with many cars

#### 13. **No Pagination**

**File:** `cars/views.py` Line: ~10  
**Issue:** No limit on car listing.
**Impact:** OOM with 1000+ cars

#### 14. **No File Upload Validation**

**File:** `cars/models.py` Line: ~98

```python
thumbnail = models.ImageField(...)  # No size/type check
```

**Impact:** DOS via large file upload

#### 15. **Price Default = 0**

**File:** `cars/models.py` Line: ~29  
**Issue:** Allows free rentals.
**Impact:** Revenue loss

#### 16. **No Overbooking Prevention**

**Issue:** Same car can be double-booked for overlapping dates.
**Impact:** Customer shows up, car not available

#### 17. **Email Errors Crash Signup**

**File:** `userAuth/utils.py` Line: ~35

```python
sg.send(message)  # No try-except
```

**Impact:** Signup fails if SendGrid is down

#### 18. **Synchronous Email (Blocks User)**

**Issue:** Email sent during HTTP request.
**Impact:** Page hangs if email service slow

#### 19. **Hardcoded FROM_EMAIL**

**File:** `Diakorentalcars/settings.py` Line: 175

```python
DEFAULT_FROM_EMAIL = "kellyjnambale@gmail.com"  # Personal email!
```

**Impact:** Unprofessional emails

### 🟡 MEDIUM SEVERITY

#### 20-30. Additional Issues:

- **No soft delete:** Hard deletes lose data permanently
- **No rate limit:** Email resend can be spammed
- **No time math:** Same-day rental pricing wrong
- **Year not validated:** Can be 9999 or 1900
- **Status transitions unrestricted:** Can go from confirmed → draft
- **User can edit is_staff:** Privilege escalation
- **No admin logging:** No audit trail
- **No CAPTCHA:** Brute force possible
- **No availability check:** Can book unavailable cars
- **Seats/Doors can be 0:** Invalid specs

---

## FIX PRIORITY

**CRITICAL (1-3 days):**

1. Authorization bypasses (#1-4)
2. DEBUG=True, SECRET_KEY, ALLOWED_HOSTS (#5-7)
3. Overbooking (#16)
4. Profile error handling (#11)

**HIGH (1 week):** 5. Query optimization (#12-13) 6. Pagination (#13) 7. Email errors (#17-18) 8. Booking workflow (#25)

**MEDIUM (2 weeks):** 9. Soft deletes (#20) 10. Rate limiting (#21) 11. Field validation (#23, #30) 12. CAPTCHA (#28)

---

## Future Enhancements

### Planned Features

- [ ] Payment gateway integration (Stripe, PayPal)
- [ ] Advanced booking filters and search
- [ ] Booking price calculation with dynamic rates
- [ ] Customer reviews and ratings
- [ ] Multi-location support
- [ ] Loyalty/rewards program
- [ ] Mobile app (React Native, Flutter)
- [ ] Real-time booking notifications
- [ ] Advanced analytics dashboard
- [ ] API (REST or GraphQL) for third-party integration

---

## Credits

**Chief Developer:** Kelly Jnambale  
**Framework:** Django (Python)  
**Frontend:** Tailwind CSS  
**Deployment:** Railway

---

## License

This project is built with passion and dedication. All rights reserved.

---

## Support & Contact

For issues, questions, or contributions, please reach out to the development team.

**Latest Update:** February 2026  
**Status:** Production Ready  
**Environment:** Railway (diakorentalcars-production.up.railway.app)
