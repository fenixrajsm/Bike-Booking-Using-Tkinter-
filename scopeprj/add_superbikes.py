import db_connection
import mysql.connector

def add_bikes():
    print("Adding Superbikes...")
    conn = db_connection.create_connection()
    if not conn:
        print("Failed to connect")
        return

    cursor = conn.cursor()
    try:
        sql = "INSERT INTO bikes (model_name, engine_cc, mileage, price, color, stock, image_path, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        bikes = [
            ("Kawasaki Ninja H2r", "998cc Supercharged", "15 kmpl", 3500000, "Mirror Coated Black", 2, "assets/ninja_h2.png", "The world's only supercharged production hypersport streetbike."),
            ("Ducati Panigale V4", "1103cc", "16 kmpl", 2700000, "Ducati Red", 3, "assets/ducati_panigale.png", "A symphony of Italian performance and emotion."),
            ("BMW S1000RR", "999cc", "17 kmpl", 2400000, "M Motorsport", 4, "assets/bmw_s1000rr.png", "The superbike of superlatives. Perfect for the track and the road.")
        ]
        
        # Check if they already exist to avoid duplicates (simple check by name)
        for bike in bikes:
            cursor.execute("SELECT id FROM bikes WHERE model_name = %s", (bike[0],))
            if not cursor.fetchone():
                cursor.execute(sql, bike)
                print(f"Added {bike[0]}")
            else:
                print(f"Skipped {bike[0]} (already exists)")

        conn.commit()
        print("Superbikes added successfully.")
    except Exception as e:
        print(f"Error adding bikes: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    add_bikes()
