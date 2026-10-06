import sqlite3
from datetime import datetime


DB_NAME = "hotel_v2.db"


STATIC_ROOMS = [
    # (room_number, room_type, price)
    (101, "Single", 1500.0),
    (102, "Single", 1500.0),
    (103, "Single", 1500.0),
    (201, "Double", 2500.0),
    (202, "Double", 2500.0),
    (203, "Double", 2500.0),
    (301, "Deluxe", 4000.0),
    (302, "Deluxe", 4000.0),
    (401, "Suite", 7000.0),
]

STATIC_FOOD_ITEMS = [
    # (service_name, price)
    ("Breakfast", 250.0),
    ("Lunch", 400.0),
    ("Dinner", 450.0),
    ("Bottled Water", 50.0),
    ("Laundry Service", 300.0),
    ("Room Cleaning (extra)", 150.0),
]


# DATABASE CONNECTION

def connect_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# CREATE TABLES 

def create_tables():

    conn = connect_db()
    cursor = conn.cursor()

    # Rooms table (static — seeded once, never inserted into again by the app)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            room_id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_number INTEGER UNIQUE NOT NULL,
            room_type TEXT NOT NULL,
            price REAL NOT NULL,
            status TEXT DEFAULT 'Available'
        )
    """)

    # Food/service menu table (static — seeded once)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS food_items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_name TEXT NOT NULL UNIQUE,
            price REAL NOT NULL
        )
    """)

    # Customers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT
        )
    """)

    # Bookings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            room_id INTEGER,
            check_in TEXT NOT NULL,
            check_out TEXT NOT NULL,
            status TEXT DEFAULT 'Booked',

            FOREIGN KEY(customer_id)
                REFERENCES customers(customer_id),

            FOREIGN KEY(room_id)
                REFERENCES rooms(room_id)
        )
    """)

    # Services table — now references food_items instead of storing a free-text price
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS services (
            service_id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER,
            item_id INTEGER,
            quantity INTEGER,

            FOREIGN KEY(booking_id)
                REFERENCES bookings(booking_id),

            FOREIGN KEY(item_id)
                REFERENCES food_items(item_id)
        )
    """)

    conn.commit()

    # Seed rooms only if empty
    cursor.execute("SELECT COUNT(*) FROM rooms")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO rooms (room_number, room_type, price)
            VALUES (?, ?, ?)
        """, STATIC_ROOMS)

    # Seed food/service menu only if empty
    cursor.execute("SELECT COUNT(*) FROM food_items")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO food_items (service_name, price)
            VALUES (?, ?)
        """, STATIC_FOOD_ITEMS)

    conn.commit()
    conn.close()

# SHOW ALL ROOMS


def show_rooms():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM rooms")
    rooms = cursor.fetchall()

    print("\n========== ROOMS ==========")

    if not rooms:
        print("No rooms found.")

    for room in rooms:
        print(
            f"ID: {room[0]} | "
            f"Room: {room[1]} | "
            f"Type: {room[2]} | "
            f"Price: ₹{room[3]} | "
            f"Status: {room[4]}"
        )

    conn.close()


# AVAILABLE ROOMS


def available_rooms():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT room_id, room_number, room_type, price
        FROM rooms
        WHERE status = 'Available'
    """)

    rooms = cursor.fetchall()

    print("\n========== AVAILABLE ROOMS ==========")

    if not rooms:
        print("No rooms are currently available.")

    for room in rooms:
        print(
            f"Room: {room[1]} | "
            f"Type: {room[2]} | "
            f"Price: ₹{room[3]}"
        )

    conn.close()


# SHOW FOOD / SERVICE MENU


def show_food_menu():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT item_id, service_name, price FROM food_items ORDER BY item_id")
    items = cursor.fetchall()

    print("\n========== FOOD / SERVICE MENU ==========")
    for item_id, name, price in items:
        print(f"{item_id}. {name} - ₹{price}")

    conn.close()
    return items

# CUSTOMER REGISTRATION


def register_customer():

    name = input("Enter customer name: ")
    phone = input("Enter phone number: ")
    email = input("Enter email: ")

    if name.strip() == "":
        print("Customer name cannot be empty.")
        return

    if phone.strip() == "":
        print("Phone number cannot be empty.")
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO customers (name, phone, email)
        VALUES (?, ?, ?)
    """, (name, phone, email))

    conn.commit()
    customer_id = cursor.lastrowid

    print("\nCustomer registered successfully.")
    print("Customer ID:", customer_id)

    conn.close()

# DATE VALIDATION


def validate_dates(check_in, check_out):

    try:
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d")

        if check_out_date <= check_in_date:
            print("Check-out date must be after check-in date.")
            return False

        return True

    
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return False

# CHECK ROOM DATE AVAILABILITY


def check_room_availability(cursor, room_id, check_in, check_out):

    cursor.execute("""
        SELECT booking_id
        FROM bookings
        WHERE room_id = ?
        AND status IN ('Booked', 'Checked-in')
        AND check_in < ?
        AND check_out > ?
    """, (room_id, check_out, check_in))

    return cursor.fetchone() is None


# BOOK ROOM


def book_room():

    try:
        customer_id = int(input("Enter customer ID: "))
        room_number = int(input("Enter room number: "))
        check_in = input("Enter check-in date (YYYY-MM-DD): ")
        check_out = input("Enter check-out date (YYYY-MM-DD): ")
    except ValueError:
        print("Please enter valid values.")
        return

    if not validate_dates(check_in, check_out):
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT customer_id FROM customers WHERE customer_id = ?", (customer_id,))
    if cursor.fetchone() is None:
        print("Customer not found.")
        conn.close()
        return

    cursor.execute("""
        SELECT room_id, price, status FROM rooms WHERE room_number = ?
    """, (room_number,))
    room = cursor.fetchone()

    if room is None:
        print("Room not found.")
        conn.close()
        return

    room_id, price, status = room

    if not check_room_availability(cursor, room_id, check_in, check_out):
        print("Sorry, this room is already booked for the selected dates.")
        print("Please choose another room or different dates.")
        conn.close()
        return

    cursor.execute("""
        INSERT INTO bookings (customer_id, room_id, check_in, check_out, status)
        VALUES (?, ?, ?, ?, 'Booked')
    """, (customer_id, room_id, check_in, check_out))

    booking_id = cursor.lastrowid

    cursor.execute("UPDATE rooms SET status = 'Booked' WHERE room_id = ?", (room_id,))

    conn.commit()

    print("\nRoom booked successfully.")
    print("Booking ID:", booking_id)

    conn.close()


# CHECK-IN


def check_in():

    try:
        booking_id = int(input("Enter booking ID: "))
    except ValueError:
        print("Invalid booking ID.")
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT room_id FROM bookings
        WHERE booking_id = ? AND status = 'Booked'
    """, (booking_id,))
    booking = cursor.fetchone()

    if booking is None:
        print("Booking not found.")
        conn.close()
        return

    room_id = booking[0]

    cursor.execute("UPDATE bookings SET status = 'Checked-in' WHERE booking_id = ?", (booking_id,))
    cursor.execute("UPDATE rooms SET status = 'Occupied' WHERE room_id = ?", (room_id,))

    conn.commit()
    print("Check-in successful.")
    conn.close()


# =========================================================
# ADD FOOD / SERVICE — now picks from the static menu instead of free-text price
# =========================================================
def add_service():
 
    conn = connect_db()
    cursor = conn.cursor()
 
    try:
        booking_id = int(input("Enter booking ID: "))
    except ValueError:
        print("Invalid booking ID.")
        conn.close()
        return
 
    cursor.execute("""
        SELECT booking_id FROM bookings
        WHERE booking_id = ? AND status IN ('Booked', 'Checked-in')
    """, (booking_id,))
    booking = cursor.fetchone()
 
    if booking is None:
        print("Booking not found or booking is already completed.")
        conn.close()
        return
 
    items = show_food_menu()  # prints menu, returns list of (item_id, name, price)
    if not items:
        conn.close()
        return
 
    valid_ids = [i[0] for i in items]
    added_lines = []  # (name, quantity, price) for the running summary
 
    # Loop so one call to this function can add several items
    # (e.g. Breakfast, then Lunch, then Bottled Water) without
    # returning to the main menu each time.
    while True:
 
        raw_item = input(
            "\nEnter item number from menu (or 'done' to finish): "
        ).strip()
 
        if raw_item.lower() == "done":
            break
 
        try:
            item_id = int(raw_item)
            quantity = int(input("Enter quantity: "))
        except ValueError:
            print("Please enter valid values.")
            continue
 
        if item_id not in valid_ids or quantity <= 0:
            print("Invalid item number or quantity.")
            continue
 
        cursor.execute("""
            INSERT INTO services (booking_id, item_id, quantity)
            VALUES (?, ?, ?)
        """, (booking_id, item_id, quantity))
 
        item_name = next(name for iid, name, price in items if iid == item_id)
        item_price = next(price for iid, name, price in items if iid == item_id)
        added_lines.append((item_name, quantity, item_price))
 
        print(f"Added: {item_name} x {quantity}")
 
    conn.commit()
    conn.close()
 
    if not added_lines:
        print("No services added.")
        return
 
    print("\n--- Services added this session ---")
    running_total = 0
    for name, quantity, price in added_lines:
        line_total = quantity * price
        running_total += line_total
        print(f"{name} x {quantity} = ₹{line_total}")
    print(f"Session total: ₹{running_total}")
    print("(Room charge and any earlier services are added at checkout.)")
 
# =========================================================
# CHECK-OUT AND BILL
# =========================================================

def check_out():

    try:
        booking_id = int(input("Enter booking ID: "))
    except ValueError:
        print("Invalid booking ID.")
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            b.room_id, b.customer_id, b.check_in, b.check_out,
            r.room_number, r.price, c.name
        FROM bookings b
        JOIN rooms r ON b.room_id = r.room_id
        JOIN customers c ON b.customer_id = c.customer_id
        WHERE b.booking_id = ?
        AND b.status IN ('Booked', 'Checked-in')
    """, (booking_id,))
    booking = cursor.fetchone()

    if booking is None:
        print("Booking not found or already checked out.")
        conn.close()
        return

    (room_id, customer_id, check_in_date, check_out_date,
     room_number, room_price, customer_name) = booking

    date1 = datetime.strptime(check_in_date, "%Y-%m-%d")
    date2 = datetime.strptime(check_out_date, "%Y-%m-%d")
    nights = (date2 - date1).days
    if nights <= 0:
        nights = 1

    room_charge = nights * room_price

    # Service charges — price now pulled from food_items, not stored per-row
    cursor.execute("""
        SELECT f.service_name, s.quantity, f.price
        FROM services s
        JOIN food_items f ON s.item_id = f.item_id
        WHERE s.booking_id = ?
    """, (booking_id,))
    services = cursor.fetchall()

    service_total = 0
    for service_name, quantity, price in services:
        service_total += quantity * price

    total = room_charge + service_total

    cursor.execute("UPDATE bookings SET status = 'Checked-out' WHERE booking_id = ?", (booking_id,))
    cursor.execute("UPDATE rooms SET status = 'Available' WHERE room_id = ?", (room_id,))

    conn.commit()

    print("\n================================")
    print("          HOTEL BILL")
    print("================================")
    print("Customer:", customer_name)
    print("Room:", room_number)
    print("Check-in:", check_in_date)
    print("Check-out:", check_out_date)
    print("Nights:", nights)
    print("--------------------------------")
    print("Room Charge: ₹", room_charge)

    print("\nServices:")
    for name, quantity, price in services:
        amount = quantity * price
        print(f"{name} x {quantity} = ₹{amount}")

    print("--------------------------------")
    print("Service Charges: ₹", service_total)
    print("TOTAL BILL: ₹", total)
    print("================================")

    conn.close()


# CANCEL BOOKING


def cancel_booking():

    try:
        booking_id = int(input("Enter booking ID: "))
    except ValueError:
        print("Invalid booking ID.")
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT room_id FROM bookings
        WHERE booking_id = ? AND status = 'Booked'
    """, (booking_id,))
    booking = cursor.fetchone()

    if booking is None:
        print("Booking not found or cannot be cancelled.")
        conn.close()
        return

    room_id = booking[0]

    cursor.execute("UPDATE bookings SET status = 'Cancelled' WHERE booking_id = ?", (booking_id,))
    cursor.execute("UPDATE rooms SET status = 'Available' WHERE room_id = ?", (room_id,))

    conn.commit()
    print("Booking cancelled successfully.")
    conn.close()


# =========================================================
# BOOKING HISTORY
# =========================================================

def booking_history():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT b.booking_id, c.name, r.room_number, b.check_in, b.check_out, b.status
        FROM bookings b
        JOIN customers c ON b.customer_id = c.customer_id
        JOIN rooms r ON b.room_id = r.room_id
        ORDER BY b.booking_id DESC
    """)
    bookings = cursor.fetchall()

    print("\n========== BOOKING HISTORY ==========")
    if not bookings:
        print("No booking history found.")

    for booking in bookings:
        print(
            f"Booking ID: {booking[0]} | "
            f"Customer: {booking[1]} | "
            f"Room: {booking[2]} | "
            f"Check-in: {booking[3]} | "
            f"Check-out: {booking[4]} | "
            f"Status: {booking[5]}"
        )

    conn.close()


# MAIN MENU  (Add Room removed — rooms/menu are static now)


def main():

    create_tables()

    while True:
        print("\n========== HOTEL RESERVATION SYSTEM ==========")
        print("1. Show All Rooms")
        print("2. Show Available Rooms")
        print("3. Show Food/Service Menu")
        print("4. Register Customer")
        print("5. Book Room")
        print("6. Check-in")
        print("7. Add Food/Service")
        print("8. Check-out & Generate Bill")
        print("9. Booking History")
        print("10. Cancel Booking")
        print("11. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            show_rooms()
        elif choice == "2":
            available_rooms()
        elif choice == "3":
            show_food_menu()
        elif choice == "4":
            register_customer()
        elif choice == "5":
            book_room()
        elif choice == "6":
            check_in()
        elif choice == "7":
            add_service()
        elif choice == "8":
            check_out()
        elif choice == "9":
            booking_history()
        elif choice == "10":
            cancel_booking()
        elif choice == "11":
            print("Thank you!")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()