import db_connection
import mysql.connector

def debug_db():
    print("--- Debugging Database ---")
    conn = db_connection.create_connection()
    if not conn:
        print("FAIL: Could not connect to DB.")
        return

    print(f"SUCCESS: Connected to {conn.database}")
    
    cursor = conn.cursor(dictionary=True)
    
    # Check tables
    try:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print("Tables found:", [t[f'Tables_in_{conn.database}'] for t in tables])
    except Exception as e:
        print("Error showing tables:", e)

    # Check Users
    try:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        print(f"Current Users count: {len(users)}")
        for u in users:
            print(f" - ID: {u['id']}, Email: {u['email']}, Pass: {u['password']}")
    except Exception as e:
        print("Error selecting users:", e)

    # Try Insert
    print("\nAttempting Test Insert...")
    try:
        from datetime import datetime
        test_email = f"test_{int(datetime.now().timestamp())}@test.com"
        cursor.execute("INSERT INTO users (name, email, password) VALUES ('Test User', %s, 'pass123')", (test_email,))
        conn.commit()
        print(f"SUCCESS: Inserted user {test_email}")
        
        # Verify
        cursor.execute("SELECT * FROM users WHERE email = %s", (test_email,))
        new_user = cursor.fetchone()
        if new_user:
            print("SUCCESS: Retrieved new user:", new_user)
        else:
            print("FAIL: Could not retrieve inserted user!")
            
    except Exception as e:
        print("Error inserting user:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    debug_db()
