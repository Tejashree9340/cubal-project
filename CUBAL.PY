# =========================
# CubaL Project FINAL
# =========================

# Install:
# pip install mysql-connector-python pandas numpy matplotlib

import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

# -------------------------
# LOGIN SYSTEM
# -------------------------
print("===== LOGIN =====")
username = input("Enter username: ")
password = input("Enter password: ")

if username == "admin" and password == "admin123":
    role = "admin"
    print("🔐 Logged in as ADMIN")
elif username == "user" and password == "user123":
    role = "user"
    print("👤 Logged in as USER")
else:
    print("❌ Invalid login")
    exit()

# -------------------------
# QUEUE
# -------------------------
request_queue = deque()

# -------------------------
# DATABASE CONNECTION
# -------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="teju123",   # change if needed
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
    print("3. View Donors")
    print("4. Search Donor")
    print("5. Exit")

    if role == "admin":
        print("6. View Requests")
        print("7. Match Donors")
        print("8. Auto Match (SQL VIEW)")
        print("9. Data Analysis")
        print("10. Process Queue")
        print("11. Show Graph")

    choice = int(input("Enter choice: "))

    # -------------------------
    # 1 REGISTER DONOR
    # -------------------------
    if choice == 1:
        name = input("Name: ")
        blood = input("Blood Group: ").upper()
        location = input("Location: ")
        contact = input("Contact: ")

        cursor.execute(
            "INSERT INTO donors (name, blood_group, location, contact) VALUES (%s,%s,%s,%s)",
            (name, blood, location, contact)
        )
        conn.commit()
        print("✅ Donor Registered")

    # -------------------------
    # 2 EMERGENCY REQUEST
    # -------------------------
    elif choice == 2:
        patient = input("Patient Name: ")
        blood = input("Blood Group: ").upper()
        location = input("Location: ")
        urgency = input("Urgency: ")

        cursor.execute(
            "INSERT INTO requests (patient_name, blood_group, location, urgency) VALUES (%s,%s,%s,%s)",
            (patient, blood, location, urgency)
        )
        conn.commit()

        request_queue.append((patient, blood, location, urgency))

        print("🚨 Request Added")

    # -------------------------
    # 3 VIEW DONORS
    # -------------------------
    elif choice == 3:
        cursor.execute("SELECT * FROM donors")
        df = pd.DataFrame(cursor.fetchall(), columns=["ID","Name","Blood","Location","Contact"])
        print(df)

    # -------------------------
    # 4 SEARCH DONOR (FIXED)
    # -------------------------
    elif choice == 4:
        blood = input("Enter Blood Group: ").upper()

        cursor.execute("SELECT * FROM donors")
        df = pd.DataFrame(cursor.fetchall(), columns=["ID","Name","Blood","Location","Contact"])

        result = df[df["Blood"].str.upper() == blood]

        print("\n--- Search Result ---")
        if result.empty:
            print(f"❌ No donor found for {blood}")
        else:
            print(result)

    # -------------------------
    # 5 EXIT
    # -------------------------
    elif choice == 5:
        print("Exiting...")
        break

    # -------------------------
    # ADMIN FEATURES
    # -------------------------
    elif role == "admin" and choice == 6:
        cursor.execute("SELECT * FROM requests")
        df = pd.DataFrame(cursor.fetchall(), columns=["ID","Patient","Blood","Location","Urgency"])
        print(df)

    elif role == "admin" and choice == 7:
        blood = input("Blood: ").upper()
        location = input("Location: ")

        cursor.execute("SELECT * FROM donors")
        df = pd.DataFrame(cursor.fetchall(), columns=["ID","Name","Blood","Location","Contact"])

        result = df[(df["Blood"] == blood) & (df["Location"] == location)]

        if result.empty:
            print("❌ No match found")
        else:
            print(result)

    elif role == "admin" and choice == 8:
        cursor.execute("SELECT * FROM donor_match")
        df = pd.DataFrame(cursor.fetchall(), columns=["Donor","Blood","Location","Contact","Patient","Urgency"])
        print(df)

    elif role == "admin" and choice == 9:
        cursor.execute("SELECT blood_group FROM donors")
        arr = np.array([x[0] for x in cursor.fetchall()])
        u, c = np.unique(arr, return_counts=True)

        print("\n--- Blood Distribution ---")
        for i, j in zip(u, c):
            print(i, ":", j)

    elif role == "admin" and choice == 10:
        if request_queue:
            print("Processing:", request_queue.popleft())
        else:
            print("Queue empty")

    elif role == "admin" and choice == 11:
        cursor.execute("SELECT blood_group FROM donors")
        arr = np.array([x[0] for x in cursor.fetchall()])
        u, c = np.unique(arr, return_counts=True)

        plt.bar(u, c)
        plt.xlabel("Blood Group")
        plt.ylabel("Donors")
        plt.title("Blood Distribution")
        plt.show()

    else:
        print("❌ Invalid choice")

# CLOSE
conn.close()