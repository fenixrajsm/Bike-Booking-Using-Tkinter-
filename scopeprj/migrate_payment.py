import db_connection
import mysql.connector

def migrate():
    print("Migrating database (Payment Method)...")
    conn = db_connection.create_connection()
    if not conn:
        print("Failed to connect")
        return

    cursor = conn.cursor()
    try:
        # Add payment_method
        try:
            cursor.execute("ALTER TABLE bookings ADD COLUMN payment_method VARCHAR(50)")
            print("Added column 'payment_method'")
        except Exception as e:
            print(f"Skipped 'payment_method' (maybe exists): {e}")
            
        conn.commit()
        print("Migration complete.")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
