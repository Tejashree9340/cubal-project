# =========================
# CubaL Project (FINAL - WITH SQL VIEW MATCHING)
# =========================

# Install:
# pip install mysql-connector-python

import mysql.connector

# -------------------------
# CONNECT DATABASE
# -------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="teju123" , # 🔥 IMPORTANT: put your MySQL password here (empty if no password),  # change this
    database="cubal"
)

cursor = conn.cursor()

# -------------------------
# MENU LOOP
# -------------------------
while True:
    print("\n===== CubaL Emergency System =====")
    print("1. Register Donor")
    print("2. Emergency Request")
    print("3. View All Donors")
    print("4. Search Donor by Blood Group")
    print("5. Exit")
    print("6. View Emergency Requests")
    print("7. Match Donors by Location")
    print("8. 🔥 Auto Match (Using SQL VIEW)")

    choice = int(input("Enter choice: "))

    # 1. REGISTER DONOR
    if choice == 1:
        name = input("Name: ")
        blood = input("Blood Group: ")
        location = input("Location: ")
        contact = input("Contact: ")

        query = "INSERT INTO donors (name, blood_group, location, contact) VALUES (%s,%s,%s,%s)"
        cursor.execute(query, (name, blood, location, contact))
        conn.commit()

        print("✅ Donor Registered Successfully")

    # 2. EMERGENCY REQUEST
    elif choice == 2:
        patient = input("Patient Name: ")
        blood = input("Blood Group: ")
        location = input("Location: ")
        urgency = input("Urgency (High/Medium/Low): ")

        query = "INSERT INTO requests (patient_name, blood_group, location, urgency) VALUES (%s,%s,%s,%s)"
        cursor.execute(query, (patient, blood, location, urgency))
        conn.commit()

        print("🚨 Emergency Request Added")

    # 3. VIEW DONORS
    elif choice == 3:
        cursor.execute("SELECT * FROM donors")
        data = cursor.fetchall()

        print("\n--- Donor List ---")
        for row in data:
            print(f"ID:{row[0]} | Name:{row[1]} | Blood:{row[2]} | Location:{row[3]} | Contact:{row[4]}")

    # 4. SEARCH DONOR
    elif choice == 4:
        blood = input("Enter Blood Group: ")

        cursor.execute("SELECT * FROM donors WHERE blood_group = %s", (blood,))
        data = cursor.fetchall()

        if data:
            print("\n--- Matching Donors ---")
            for row in data:
                print(f"Name:{row[1]} | Location:{row[3]} | Contact:{row[4]}")
        else:
            print("❌ No donors found")

    # 5. EXIT
    elif choice == 5:
        print("Exiting CubaL...")
        break

    # 6. VIEW EMERGENCY REQUESTS
    elif choice == 6:
        cursor.execute("SELECT * FROM requests")
        data = cursor.fetchall()

        print("\n--- Emergency Requests ---")
        for row in data:
            print(f"Patient:{row[1]} | Blood:{row[2]} | Location:{row[3]} | Urgency:{row[4]}")

    # 7. MATCH DONORS BY LOCATION
    elif choice == 7:
        blood = input("Enter Blood Group: ")
        location = input("Enter Location: ")

        query = "SELECT * FROM donors WHERE blood_group = %s AND location = %s"
        cursor.execute(query, (blood, location))
        data = cursor.fetchall()

        if data:
            print("\n--- Matched Donors ---")
            for row in data:
                print(f"Name:{row[1]} | Location:{row[3]} | Contact:{row[4]}")
        else:
            print("❌ No matching donors found")

    # 8. 🔥 AUTO MATCH USING SQL VIEW
    elif choice == 8:
        cursor.execute("SELECT * FROM donor_match")
        data = cursor.fetchall()

        print("\n🔥 --- AUTO MATCHED DONORS ---")
        for row in data:
            print(f"Donor:{row[0]} | Blood:{row[1]} | Location:{row[2]} | Contact:{row[3]} | Patient:{row[4]} | Urgency:{row[5]}")

    else:
        print("Invalid choice")

# CLOSE CONNECTION
conn.close()
