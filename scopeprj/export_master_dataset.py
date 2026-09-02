import mysql.connector
import csv
import os
from db_connection import create_connection

def export_master_dataset():
    """Exports a denormalized master dataset (Bookings + Users + Bikes) to CSV."""
    conn = create_connection()
    if not conn:
        print("Failed to connect to the database.")
        return

    # Create output directory
    output_dir = 'exported_data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        cursor = conn.cursor()
        
        # SQL Query to join tables
        query = """
        SELECT 
            b.id as booking_id,
            b.booking_date,
            b.status,
            b.payment_method,
            u.id as user_id,
            u.name as user_name,
            u.email as user_email,
            u.phone as user_phone,
            u.address as user_address,
            bk.id as bike_id,
            bk.model_name as bike_model,
            bk.price as bike_price,
            bk.engine_cc as bike_engine,
            bk.color as bike_color
        FROM bookings b
        LEFT JOIN users u ON b.user_id = u.id
        LEFT JOIN bikes bk ON b.bike_id = bk.id
        ORDER BY b.booking_date DESC
        """
        
        print("Executing query to join Bookings, Users, and Bikes...")
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Get column names
        column_names = [i[0] for i in cursor.description]
        
        # Define CSV file path
        csv_file_path = os.path.join(output_dir, "master_dataset.csv")
        
        # Write to CSV
        try:
            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(column_names)
                writer.writerows(rows)
                
            print(f"Successfully exported master dataset to {csv_file_path}")
            print(f"Total records exported: {len(rows)}")
            
        except Exception as e:
            print(f"Error writing to {csv_file_path}: {e}")

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    export_master_dataset()
