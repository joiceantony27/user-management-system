# User Management System

A full-stack web application for managing user accounts with role-based access control (RBAC). Built with Django REST Framework backend and React frontend.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Django](https://img.shields.io/badge/django-4.2-green.svg)
![React](https://img.shields.io/badge/react-18.2-blue.svg)

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Environment Variables](#environment-variables)
- [API Documentation](#api-documentation)
- [Deployment Instructions](#deployment-instructions)
- [Testing](#testing)
- [Live Demo](#live-demo)

## 🎯 Project Overview

The User Management System is a web application that provides:
- User authentication with JWT tokens
- Role-based access control (Admin/User)
- User lifecycle management (activate/deactivate accounts)
- Profile management
- Admin dashboard for user management

## ✨ Features

### Authentication
- ✅ User signup with email validation
- ✅ Strong password requirements
- ✅ JWT-based authentication
- ✅ Token refresh mechanism
- ✅ Secure logout with token blacklisting

### User Features
- ✅ View and edit profile
- ✅ Change password
- ✅ Dashboard overview

### Admin Features
- ✅ View all users with pagination
- ✅ Filter users by status and role
- ✅ Search users by name or email
- ✅ Activate/deactivate user accounts
- ✅ Role-based access control

### Security
- ✅ Password hashing with Argon2
- ✅ JWT authentication
- ✅ Protected API routes
- ✅ Input validation
- ✅ CORS configuration
- ✅ Environment variables for secrets

### UI/UX
- ✅ Responsive design (mobile & desktop)
- ✅ Toast notifications
- ✅ Loading states
- ✅ Form validation
- ✅ Confirmation modals
- ✅ Clean, modern interface

## 🛠 Tech Stack

### Backend
- **Framework:** Django 4.2, Django REST Framework
- **Authentication:** Simple JWT
- **Database:** PostgreSQL (production) / SQLite (development)
- **Password Hashing:** Argon2
- **CORS:** django-cors-headers
- **WSGI Server:** Gunicorn

### Frontend
- **Framework:** React 18 with Hooks
- **Routing:** React Router v6
- **HTTP Client:** Axios
- **Notifications:** React Hot Toast
- **Styling:** Custom CSS (no framework)

### Deployment
- **Backend:** Render / Railway
- **Frontend:** Vercel / Netlify
- **Database:** PostgreSQL (Neon / Railway / Render)

## 📁 Project Structure

```
user-management-system/
├── backend/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── users/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── exceptions.py
│   │   ├── models.py
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── manage.py
│   ├── requirements.txt
│   ├── Procfile
│   ├── runtime.txt
│   ├── .env.example
│   └── .gitignore
│
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   ├── manifest.json
│   │   └── robots.txt
│   ├── src/
│   │   ├── components/
│   │   │   ├── Layout.js
│   │   │   ├── Layout.css
│   │   │   ├── LoadingSpinner.js
│   │   │   ├── Modal.js
│   │   │   ├── Pagination.js
│   │   │   └── ProtectedRoute.js
│   │   ├── context/
│   │   │   └── AuthContext.js
│   │   ├── pages/
│   │   │   ├── Login.js
│   │   │   ├── Signup.js
│   │   │   ├── Dashboard.js
│   │   │   ├── Profile.js
│   │   │   ├── AdminDashboard.js
│   │   │   ├── Auth.css
│   │   │   ├── Dashboard.css
│   │   │   ├── Profile.css
│   │   │   └── AdminDashboard.css
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.js
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   ├── .env.example
│   └── .gitignore
│
└── README.md
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn
- PostgreSQL (optional, SQLite for development)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment file:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your configuration.

5. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (admin):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server:**
   ```bash
   python manage.py runserver
   ```
   
   Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create environment file:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` to set the API URL.

4. **Run development server:**
   ```bash
   npm start
   ```
   
   Frontend will be available at `http://localhost:3000`

## 🔐 Environment Variables

### Backend (.env)

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `your-secret-key-here` |
| `DEBUG` | Debug mode | `True` or `False` |
| `ALLOWED_HOSTS` | Allowed hosts | `localhost,127.0.0.1` |
| `DATABASE_URL` | PostgreSQL connection URL | `postgres://user:pass@host/db` |
| `JWT_SECRET_KEY` | JWT signing key | `your-jwt-secret` |
| `JWT_ACCESS_TOKEN_LIFETIME` | Access token lifetime (minutes) | `60` |
| `JWT_REFRESH_TOKEN_LIFETIME` | Refresh token lifetime (minutes) | `1440` |
| `CORS_ALLOWED_ORIGINS` | Allowed frontend origins | `http://localhost:3000` |

### Frontend (.env)

| Variable | Description | Example |
|----------|-------------|---------|
| `REACT_APP_API_URL` | Backend API URL | `http://localhost:8000/api` |
| `REACT_APP_NAME` | Application name | `User Management System` |

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Authentication Endpoints

#### Sign Up
```http
POST /auth/signup/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "StrongPass123!",
  "confirm_password": "StrongPass123!",
  "full_name": "John Doe"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "User registered successfully.",
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "full_name": "John Doe",
      "role": "user",
      "status": "active",
      "created_at": "2025-12-29T10:00:00Z"
    },
    "tokens": {
      "access": "eyJ...",
      "refresh": "eyJ..."
    }
  }
}
```

#### Login
```http
POST /auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "StrongPass123!"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Login successful.",
  "data": {
    "user": {...},
    "tokens": {
      "access": "eyJ...",
      "refresh": "eyJ..."
    }
  }
}
```

#### Logout
```http
POST /auth/logout/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "refresh": "<refresh_token>"
}
```

#### Get Current User
```http
GET /auth/me/
Authorization: Bearer <access_token>
```

#### Refresh Token
```http
POST /auth/token/refresh/
Content-Type: application/json

{
  "refresh": "<refresh_token>"
}
```

### User Endpoints

#### Get Profile
```http
GET /users/profile/
Authorization: Bearer <access_token>
```

#### Update Profile
```http
PUT /users/profile/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "full_name": "John Updated",
  "email": "newemail@example.com"
}
```

#### Change Password
```http
POST /users/change-password/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "current_password": "OldPass123!",
  "new_password": "NewPass123!",
  "confirm_new_password": "NewPass123!"
}
```

### Admin Endpoints

#### List Users (Paginated)
```http
GET /admin/users/?page=1&status=active&role=user&search=john
Authorization: Bearer <admin_access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Users retrieved successfully.",
  "data": {
    "count": 25,
    "next": "http://localhost:8000/api/admin/users/?page=2",
    "previous": null,
    "users": [...]
  }
}
```

#### Activate User
```http
POST /admin/users/{user_id}/activate/
Authorization: Bearer <admin_access_token>
```

#### Deactivate User
```http
POST /admin/users/{user_id}/deactivate/
Authorization: Bearer <admin_access_token>
```

### Error Response Format
```json
{
  "success": false,
  "message": "Error description",
  "errors": {
    "field_name": ["Error message"]
  }
}
```

## 🚢 Deployment Instructions

### Backend Deployment (Render)

1. **Create a new Web Service on Render**

2. **Connect your GitHub repository**

3. **Configure build settings:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn core.wsgi:application`

4. **Set environment variables:**
   - Add all variables from `.env.example`
   - Set `DEBUG=False`
   - Set `ALLOWED_HOSTS` to include your Render domain

5. **Add PostgreSQL database:**
   - Create a new PostgreSQL instance on Render
   - Copy the Internal Database URL to `DATABASE_URL`

### Frontend Deployment (Vercel)

1. **Import your repository on Vercel**

2. **Configure build settings:**
   - Framework Preset: Create React App
   - Build Command: `npm run build`
   - Output Directory: `build`

3. **Set environment variables:**
   - `REACT_APP_API_URL`: Your deployed backend URL

4. **Deploy**

## 🧪 Testing

### Run Backend Tests

```bash
cd backend
python manage.py test users
```

**Test Coverage:**
- User model tests (create user, superuser, activate/deactivate)
- Authentication tests (signup, login, logout)
- Profile tests (update profile, change password)
- Admin tests (list users, activate/deactivate)

### Run Frontend Tests

```bash
cd frontend
npm test
```

## 🌐 Live Demo

- **Frontend URL:** [Add your deployed frontend URL]
- **Backend API:** [Add your deployed backend URL]
- **API Documentation:** [Add your API docs URL]

### Demo Credentials

**Admin Account:**
- Email: admin@example.com
- Password: AdminPass123!

**User Account:**
- Email: user@example.com
- Password: UserPass123!

## 📝 License

This project is licensed under the MIT License.

## 👤 Author

[Your Name]

---

*Built for Purple Merit Technologies Backend Developer Intern Assessment*
