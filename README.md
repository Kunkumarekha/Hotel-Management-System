# 🏨 Hotel Reservation System

A Python and SQLite-based Hotel Reservation System that manages rooms, customers, bookings, hotel services, check-in/check-out, billing, booking cancellation, and booking history.

## 📌 Project Overview

This project is a console-based hotel management application developed using Python and SQLite. It provides a simple way to manage hotel room reservations and customer services through a menu-driven interface.

The application uses SQLite database tables for rooms, customers, bookings, food/services, and service selections.

## 🚀 Features

- View all hotel rooms
- View available rooms
- View food and service menu
- Register customers
- Book rooms
- Check room availability by date
- Check-in customers
- Add food/hotel services
- Check-out customers
- Generate hotel bills
- Cancel bookings
- View booking history
- Automatically update room status
- Store data in SQLite database

## 🛠️ Technologies Used

- Python 3
- SQLite3
- SQL
- Datetime module

## 🗄️ Database

The project uses SQLite with the database:

`hotel_v2.db`

The system manages the following tables:

- Rooms
- Food Items
- Customers
- Bookings
- Services

Foreign keys are used to maintain relationships between the tables.

## 🏨 Room Types

The system contains predefined rooms such as:

- Single
- Double
- Deluxe
- Suite

Each room type has a different price.

## 🍽️ Hotel Services

Available services include:

- Breakfast
- Lunch
- Dinner
- Bottled Water
- Laundry Service
- Extra Room Cleaning

## 🔄 Booking Workflow

```text
Register Customer
       ↓
Select Room
       ↓
Enter Check-in / Check-out Dates
       ↓
Check Room Availability
       ↓
Book Room
       ↓
Check-in
       ↓
Add Food / Services
       ↓
Check-out
       ↓
Generate Bill


## 📋 Main Menu
1. Show All Rooms
2. Show Available Rooms
3. Show Food/Service Menu
4. Register Customer
5. Book Room
6. Check-in
7. Add Food/Service
8. Check-out & Generate Bill
9. Booking History
10. Cancel Booking
11. Exit

## ▶️ How to Run
1. Install Python
Make sure Python 3 is installed on your system.
2. Clone the Repository
git clone <your-github-repository-url>

3. Open the Project Folder
cd hotel-reservation-system

4. Run the Program
python hotel.py

🎯 Learning Outcomes
Python Programming
Practiced Python fundamentals including functions, loops, conditional statements, and exception handling.
SQLite Database
Learned how to create tables, insert data, update records, retrieve data, and manage a SQLite database using Python.
SQL Queries
Practiced SQL operations such as SELECT, INSERT, and UPDATE, along with joins and filtering.
CRUD Operations
Implemented Create, Read, Update, and Delete-style database operations for managing hotel data.
Database Relationships
Worked with primary keys and foreign keys to establish relationships between customers, rooms, bookings, and services.
Data Validation
Implemented validation for customer details, booking information, and check-in/check-out dates.
Real-World Application
Built a practical hotel reservation system that demonstrates how Python and databases can be combined to solve a real-world problem.
👩‍💻 Author
Kunkumarekha Udayana
B.Tech – Electronics & Communication Engineering
Python | SQL | SQLite | MySQL
