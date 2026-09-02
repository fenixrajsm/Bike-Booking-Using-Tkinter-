import db_connection
import mysql.connector

def add_20_bikes():
    print("Adding 20 Superbikes...")
    conn = db_connection.create_connection()
    if not conn:
        print("Failed to connect")
        return

    cursor = conn.cursor()
    
    # Using existing images cyclically since generation quota is reached
    img_h2 = "assets/ninja_h2.png"
    img_panigale = "assets/ducati_panigale.png"
    img_bmw = "assets/bmw_s1000rr.png"
    
    # Mapping roughly by style/brand to available images
    bikes_data = [
        ("Yamaha YZF-R1M", "998cc", "14 kmpl", 2800000, "Silver/Blue Carbon", 5, img_bmw, " MotoGP-derived crossplane crankshaft engine."),
        ("Suzuki Hayabusa", "1340cc", "11 kmpl", 1690000, "Metallic White", 10, img_h2, "The ultimate sportbike, legendary performance."), # H2 is distinct but acts as placeholder for 'fast/bulky'
        ("Honda CBR1000RR-R", "1000cc", "15 kmpl", 3300000, "Grand Prix Red", 3, img_panigale, "Born to race."),
        ("Aprilia RSV4 Factory", "1099cc", "13 kmpl", 2500000, "Aprilia Black", 4, img_panigale, "V4 engine with pure racing DNA."),
        ("MV Agusta F4 RR", "998cc", "12 kmpl", 3800000, "Red/Silver", 2, img_panigale, "Motorcycle art."),
        ("Kawasaki ZX-10R", "998cc", "15 kmpl", 1600000, "KRT Green", 8, img_h2, "World Superbike Champion."),
        ("Ducati Streetfighter V4", "1103cc", "14 kmpl", 2200000, "Dark Stealth", 5, img_panigale, "The Fight Formula."),
        ("Triumph Rocket 3", "2458cc", "10 kmpl", 2000000, "Phantom Black", 6, img_bmw, "The largest production motorcycle engine."),
        ("Indian FTR 1200", "1203cc", "18 kmpl", 1800000, "Race Replica", 6, img_h2, "Flat tracker style for the street."),
        ("Harley-Davidson Fat Boy", "1868cc", "14 kmpl", 2100000, "Vivid Black", 7, img_h2, "The original fat custom icon."),
        ("KTM 1290 Super Duke R", "1301cc", "15 kmpl", 1900000, "Orange/Blue", 5, img_panigale, "The Beast."),
        ("Yamaha MT-10 SP", "998cc", "12 kmpl", 1500000, "Icon Performance", 8, img_bmw, "Hyper Naked."),
        ("Suzuki GSX-R1000R", "1000cc", "15 kmpl", 1900000, "Metallic Triton Blue", 4, img_bmw, "Own the racetrack."),
        ("Honda Gold Wing", "1833cc", "14 kmpl", 3900000, "Gunmetal Black", 3, img_h2, "The ultimate touring machine."),
        ("BMW M 1000 RR", "999cc", "16 kmpl", 4200000, "Light White", 2, img_bmw, "Pure racing technology."),
        ("Ducati Diavel 1260", "1262cc", "15 kmpl", 2100000, "Total Black", 6, img_panigale, "Muscular silhouette."),
        ("Triumph Speed Triple 1200", "1160cc", "17 kmpl", 1700000, "Matt Silver", 5, img_bmw, "The most powerful Speed Triple ever."),
        ("Benelli TNT 600i", "600cc", "19 kmpl", 650000, "Red", 15, img_panigale, "Naked streetfighter."),
        ("Kawasaki Z900", "948cc", "17 kmpl", 900000, "Metallic Graphite", 12, img_h2, "Supernaked."),
        ("Norton Commando 961", "961cc", "18 kmpl", 2300000, "Manx Silver", 3, img_bmw, "Modern classic.")
    ]

    try:
        sql = "INSERT INTO bikes (model_name, engine_cc, mileage, price, color, stock, image_path, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        
        for bike in bikes_data:
            # Check for duplicates by name
            cursor.execute("SELECT id FROM bikes WHERE model_name = %s", (bike[0],))
            if not cursor.fetchone():
                cursor.execute(sql, bike)
                print(f"Added {bike[0]}")
            else:
                print(f"Skipped {bike[0]} (already exists)")

        conn.commit()
        print("20 Superbikes process completed.")
    except Exception as e:
        print(f"Error adding bikes: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    add_20_bikes()
