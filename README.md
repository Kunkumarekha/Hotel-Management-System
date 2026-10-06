🏨 Hotel Reservation System
A Python and SQLite-based Hotel Reservation System that manages rooms, customers, bookings, hotel services, check-in/check-out, billing, booking cancellation, and booking history.
📌 Project Overview
This project is a console-based hotel management application developed using Python and SQLite. It provides a simple way to manage hotel room reservations and customer services through a menu-driven interface.
The application uses SQLite database tables for rooms, customers, bookings, food/services, and service selections.    Pasted markdown
🚀 Features
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
- Store all data in SQLite database
The main menu provides these operations through 11 options.    Pasted markdown
🛠️ Technologies Used
- Python 3
- SQLite3
- SQL
- Datetime module
🗄️ Database
The project uses SQLite with the database:
hotel_v2.db

The system creates and manages tables for:
- Rooms
- Food Items
- Customers
- Bookings
- Services
Foreign keys are enabled to maintain relationships between the tables.    Pasted markdown
🏨 Room Types
The system contains predefined rooms such as:
- Single
- Double
- Deluxe
- Suite
with different room prices.    Pasted markdown
🍽️ Hotel Services
Available services include:
- Breakfast
- Lunch
- Dinner
- Bottled Water
- Laundry Service
- Extra Room Cleaning
   Pasted markdown
🔄 Booking Workflow
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

The system validates dates and prevents overlapping bookings for the same room.    Pasted markdown    Pasted markdown
💰 Billing
During checkout, the system calculates:
- Number of nights
- Room charges
- Food/service charges
- Total bill
The room charge is calculated based on the number of nights, while service charges are calculated using the selected quantity and service price.    Pasted markdown

3. Open the project folder
cd hotel-reservation-system

4. Run the program
python hotel.py

The SQLite database will be created automatically when the application starts.
📋 Main Menu
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

🎯 Learning Outcomes
Through this project, I practiced:
- Python programming
- Functions
- Conditional statements
- Loops
- Exception handling
- SQLite database operations
- SQL queries
- CRUD operations
- Primary and foreign keys
- Table relationships
- Date validation
- Data validation
- Real-world project workflow
👩‍💻 Author
Kunkumarekha Udayana
B.Tech – Electronics & Communication Engineering
Python | SQL | SQLite | MySQL
