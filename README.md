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


## 👩‍💻 Author
Kunkumarekha Udayana
B.Tech – Electronics & Communication Engineering
Python | SQL | SQLite | MySQL
```
