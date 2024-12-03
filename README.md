# Event Management System Backend

This project is a backend system for an event management application.
It provides RESTful APIs for user registration, login, and preference management using Flask, SQLAlchemy, and a Microsoft SQL Server database.

---

## Features

- **User Authentication**: 
  - Register new users with a name, email, and password.
  - Secure login for existing users.

- **User Preferences**: 
  - Save and manage user-specific preferences.
  - Retrieve user preferences for personalized experiences.

- **Database Integration**: 
  - Microsoft SQL Server is used to store and manage data.
  - Implements a relational database design for users and their preferences.

---

## Technologies Used

- **Backend Framework**: Flask
- **Database**: Microsoft SQL Server
- **ORM**: SQLAlchemy
- **Other Tools**: Flask-CORS, PyODBC

---

## Prerequisites

1. **Python 3.8+**
2. **Microsoft SQL Server**
3. **ODBC Driver 17 for SQL Server**
4. **Required Python Libraries**:
   - `Flask`
   - `Flask-CORS`
   - `Flask-SQLAlchemy`
   - `pyodbc`

Install the Python dependencies using:

```bash
pip install -r requirements.txt
