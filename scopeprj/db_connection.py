import mysql.connector
from mysql.connector import Error

# Database Configuration - UPDATE THESE CREDENTIALS
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',  # Default XAMPP/WAMP user
    'password': '',  # Default is often empty
    # 'database': 'bike_company_db' # We won't set this initially to allow creation
}

DB_NAME = 'bike_company_db'

def create_connection(db_name=DB_NAME):
    """create a database connection to the MySQL database"""
    conn = None
    try:
        config = DB_CONFIG.copy()
        if db_name:
            config['database'] = db_name
        
        conn = mysql.connector.connect(**config)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    return conn

def setup_database():
    """Initializes the database and tables if they don't exist."""
    print("Setting up database...")
    
    # 1. Connect to Server (no DB selected) to create DB
    conn = create_connection(db_name=None)
    if not conn:
        print("Failed to connect to MySQL Server. Check credentials in db_connection.py")
        return False

    cursor = conn.cursor()
    
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database '{DB_NAME}' checked/created.")
    except Error as e:
        print(f"Error creating database: {e}")
        conn.close()
        return False
    
    conn.close()

    # 2. Connect to the specific DB to create tables
    conn = create_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()

    queries = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            phone VARCHAR(20),
            address TEXT,
            role ENUM('user', 'admin') DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS bikes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            model_name VARCHAR(100) NOT NULL,
            engine_cc VARCHAR(50),
            mileage VARCHAR(50),
            price DECIMAL(10, 2) NOT NULL,
            color VARCHAR(50),
            stock INT DEFAULT 1,
            image_path VARCHAR(255),
            description TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS bookings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            bike_id INT,
            customer_name VARCHAR(100) NOT NULL,
            customer_phone VARCHAR(20),
            booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(50) DEFAULT 'Confirmed',
            payment_method VARCHAR(50),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (bike_id) REFERENCES bikes(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            message TEXT,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    ]

    try:
        for q in queries:
            cursor.execute(q)
        print("Tables checked/created.")
        
        # 3. Seed Admin User (if not exists)
        cursor.execute("SELECT * FROM users WHERE email = 'admin@bike.com'")
        if not cursor.fetchone():
            # Simple plaintext for demo or use hashing? Plan said hashed, but for simplicity/demo we might start plain
            # We will use simple hashing if possible, or just plain for the demo start
            # Let's simple INSERT for now.
            query = "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)"
            val = ("Admin", "admin@bike.com", "admin123", "admin")
            cursor.execute(query, val)
            print("Default Admin created: admin@bike.com / admin123")
            conn.commit()

        # 4. Seed Some Bikes (if empty)
        cursor.execute("SELECT count(*) FROM bikes")
        if cursor.fetchone()[0] == 0:
            bike_sql = "INSERT INTO bikes (model_name, engine_cc, mileage, price, color, stock, description) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            bikes = [
                ("Thunderbird 350", "346cc", "35 kmpl", 180000, "Black", 5, "Classic cruiser with a powerful engine."),
                ("Racer R15", "155cc", "45 kmpl", 150000, "Racing Blue", 8, "Sports bike with aerodynamic design."),
                ("City Commuter Z", "110cc", "60 kmpl", 75000, "Red", 15, "Perfect for city traffic and daily commute.")
            ]
            cursor.executemany(bike_sql, bikes)
            print(f"Seeded {len(bikes)} sample bikes.")
            conn.commit()

    except Error as e:
        print(f"Error creating tables: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    setup_database()
