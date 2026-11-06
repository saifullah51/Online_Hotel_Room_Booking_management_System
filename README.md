# 🏨 Online Hotel Management System

A simple **Online Hotel Management System** developed using **Python Flask, MySQL, HTML, CSS, and JavaScript**. The system allows customers to register, log in, view available rooms, book rooms, view their bookings, and cancel reservations.

## 📌 Project Overview

The Online Hotel Management System provides a web-based platform for managing hotel room reservations.

Customers can:

- Create an account
- Login securely
- View available hotel rooms
- View room type, price, capacity, and status
- Book a room for selected dates
- Calculate the total booking amount automatically
- View their booking history
- Cancel confirmed bookings
- Logout from the system

The application uses **Flask as the backend** and **MySQL as the database**.

---

## 🚀 Features

### 👤 Customer Management

- Customer registration
- Customer login
- Session-based authentication
- Customer logout
- Duplicate email checking

### 🏨 Room Management

- Display available hotel rooms
- Display room number
- Display room type
- Display room capacity
- Display room price
- Display room availability status

### 📅 Booking Management

- Select a room
- Select check-in date
- Select check-out date
- Automatic calculation of number of nights
- Automatic calculation of total amount
- Prevent overlapping bookings
- Generate booking ID
- View booking details

### ❌ Cancellation

- Customers can cancel their confirmed bookings
- Cancelled bookings remain stored in the database
- Booking status changes from `Confirmed` to `Cancelled`

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web framework |
| MySQL | Database |
| HTML5 | Web page structure |
| CSS3 | Website styling |
| JavaScript | Client-side functionality |
| mysql-connector-python | Flask–MySQL connection |
| VS Code | Development environment |
| Git | Version control |
| GitHub | Project repository |

---

## 📂 Project Structure

```text
Online-Hotel-Management-System/
│
├── app.py
│
├── database.py
│
├── requirements.txt
│
├── .gitignore
│
├── templates/
│   ├── index.html
│   ├── rooms.html
│   ├── register.html
│   ├── login.html
│   ├── booking.html
│   ├── booking_success.html
│   └── bookings.html
│
├── static/
│   └── css/
│       └── style.css
│
└── database/
    └── hotel_management.sql
```

---

## 🗄️ Database

The project uses a MySQL database named:

```text
hotel_management
```

### Tables

#### Customer

Stores customer registration information.

```text
customer_id
name
email
phone
password
```

#### Room

Stores hotel room information.

```text
room_id
room_number
room_type
price
capacity
status
```

#### Booking

Stores customer room reservations.

```text
booking_id
customer_id
room_id
check_in
check_out
total_amount
status
```

### Database Relationship

```text
Customer
   │
   │ customer_id
   │
   ▼
Booking
   │
   │ room_id
   │
   ▼
Room
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/saifullah51/Online-Hotel-Management-System.git
```

Move into the project directory:

```bash
cd Online-Hotel-Management-System
```

### 2. Install required packages

```bash
pip install -r requirements.txt
```

If required, install manually:

```bash
pip install flask mysql-connector-python
```

---

## 🗄️ MySQL Configuration

Open MySQL Workbench and create the database:

```sql
CREATE DATABASE hotel_management;
```

Then select it:

```sql
USE hotel_management;
```

Create the required tables using the SQL file provided in:

```text
database/hotel_management.sql
```

---

## 🔐 Database Connection

Open:

```text
database.py
```

Configure your local MySQL credentials:

```python
import mysql.connector

def get_db_connection():

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_MYSQL_PASSWORD",
        database="hotel_management"
    )

    return connection
```

Replace:

```text
YOUR_MYSQL_PASSWORD
```

with your local MySQL password.

**Do not upload your actual database password to GitHub.**

---

## ▶️ Running the Application

Start the Flask server:

```bash
python app.py
```

The application will run at:

```text
http://127.0.0.1:5005
```

Open the URL in your web browser.

---

## 🔄 Application Flow

```text
                HOME
                 │
                 ▼
              ROOMS
                 │
        ┌────────┴────────┐
        │                 │
      LOGIN            REGISTER
        │                 │
        └────────┬────────┘
                 │
                
