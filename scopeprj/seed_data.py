import mysql.connector
import random
from db_connection import create_connection
import datetime

def seed_data():
    conn = create_connection()
    if not conn:
        print("Failed to connect to the database.")
        return

    cursor = conn.cursor()
    
    # 1. Add Fake Users
    users = [
        ("John Doe", "john.doe@example.com", "password123", "555-0101", "123 Maple St, Springfield"),
        ("Jane Smith", "jane.smith@example.com", "securepass", "555-0102", "456 Oak Ave, Metropolis"),
        ("Alice Johnson", "alice.j@example.com", "alice2024", "555-0103", "789 Pine Rd, Gotham"),
        ("Bob Brown", "bob.brown@example.com", "bobbyb", "555-0104", "321 Elm St, Smallville"),
        ("Charlie Davis", "charlie.d@example.com", "charlie1", "555-0105", "654 Cedar Ln, Star City"),
        ("Diana Prince", "diana.prince@example.com", "wonderwoman", "555-0106", "987 Birch Blvd, Themyscira"),
        ("Evan Wright", "evan.wright@example.com", "evanw", "555-0107", "159 Walnut Dr, Central City"),
        ("Fiona Green", "fiona.green@example.com", "fiona123", "555-0108", "753 Spruce Ct, Coast City")
    ]
    
    print("Seeding Users...")
    user_ids = []
    try:
        for name, email, pwd, phone, addr in users:
            # Check if user exists
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            result = cursor.fetchone()
            if result:
                user_ids.append(result[0])
                print(f"User {name} already exists.")
            else:
                cursor.execute(
                    "INSERT INTO users (name, email, password, phone, address, role) VALUES (%s, %s, %s, %s, %s, 'user')",
                    (name, email, pwd, phone, addr)
                )
                user_ids.append(cursor.lastrowid)
                print(f"Added user: {name}")
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Error seeding users: {e}")

    # 2. Add Fake Bookings
    # Get Bike IDs
    cursor.execute("SELECT id FROM bikes")
    bike_ids = [row[0] for row in cursor.fetchall()]
    
    if not bike_ids:
        print("No bikes found. Cannot seed bookings.")
        return

    print("\nSeeding Bookings...")
    
    statuses = ['Confirmed', 'Pending', 'Cancelled', 'Completed']
    payment_methods = ['Cash', 'Card', 'UPI', 'Net Banking']
    
    try:
        # Create 15 random bookings
        for _ in range(15):
            user_id = random.choice(user_ids)
            bike_id = random.choice(bike_ids)
            
            # Fetch user details for booking (simulating user entering data)
            cursor.execute("SELECT name, phone FROM users WHERE id = %s", (user_id,))
            u_name, u_phone = cursor.fetchone()
            
            # Random date within last 30 days
            days_ago = random.randint(0, 30)
            booking_date = datetime.datetime.now() - datetime.timedelta(days=days_ago)
            
            status = random.choice(statuses)
            payment = random.choice(payment_methods)
            
            cursor.execute(
                """INSERT INTO bookings 
                (user_id, bike_id, customer_name, customer_phone, booking_date, status, payment_method) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (user_id, bike_id, u_name, u_phone, booking_date, status, payment)
            )
            print(f"Added booking for {u_name} - Status: {status}")
            
        conn.commit()
        print("\nSeeding Completed Successfully.")
        
    except mysql.connector.Error as e:
        print(f"Error seeding bookings: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    seed_data()
