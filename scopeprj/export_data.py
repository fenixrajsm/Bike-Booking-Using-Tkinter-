import mysql.connector
import csv
import os
from db_connection import create_connection

def export_tables_to_csv():
    """Exports all tables from the database to CSV files in a specific directory."""
    conn = create_connection()
    if not conn:
        print("Failed to connect to the database.")
        return

    # Create output directory
    output_dir = 'exported_data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    try:
        cursor = conn.cursor()
        
        # Get list of all tables
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        
        if not tables:
            print("No tables found in the database.")
            return

        print(f"Found tables: {', '.join(tables)}")

        for table_name in tables:
            print(f"Exporting table: {table_name}...")
            
            # Fetch all data from the table
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            # Get column names
            column_names = [i[0] for i in cursor.description]
            
            # Define CSV file path
            csv_file_path = os.path.join(output_dir, f"{table_name}.csv")
            
            # Write key table data to CSV file
            try:
                with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)
                    
                    # Write header
                    writer.writerow(column_names)
                    
                    # Write rows
                    writer.writerows(rows)
                    
                print(f"Successfully exported {table_name} to {csv_file_path}")
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
    export_tables_to_csv()
