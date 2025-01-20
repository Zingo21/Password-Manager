import os
import hashlib
import secrets
import string
import sqlite3
import getpass
import base64

def load_key(main_password):
    key = hashlib.sha256(main_password.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(key)

def save_main_password(main_password):
    hashed_password = hashlib.sha256(main_password.encode('utf-8')).hexdigest()
    with open as f:
        f.write(hashed_password)

def verify_main_password(main_password):
    with open('password.txt', 'r') as f:
        saved_hash = f.read().strip()
    return hashlib.sha256(main_password.encode('utf-8')).hexdigest() == saved_hash

def initialize_main_password():
    if not os.path.exists('password.txt'):
        print("No main password found. Let's set it up!")
        return create_main_password()
    else:
        while True:
            main_password = getpass.getpass("Enter your main password: ")
            if verify_main_password(main_password):
                print("Main password has been verified!")
                return main_password
            else:
                print("Invalid password, please try again.")

def create_main_password():
    while True:
        main_password = getpass.getpass("Enter your new password: ")
        confirm_password = getpass.getpass("Confirm password: ")
        if main_password == confirm_password:
            hashed_password = hashlib.sha256(main_password.encode('utf-8')).hexdigest()
            with open('password.txt', 'w') as f:
                f.write(hashed_password)
            print("Main password has been set!")
            return main_password
        else:
            print("Passwords do not match, please try again.")

def generate_password(length=12):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY,
            service TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_password(service, username, encrypted_password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passwords (service, username, password) VALUES (?, ?, ?)", (service, username, encrypted_password))
    conn.commit()
    conn.close()

def get_password(service, cipher):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM passwords WHERE service=?", (service,))
    result = cursor.fetchone()
    if result:
        username, encrypted_password = result
        password = cipher.decrypt(encrypted_password).decode('utf-8')
        return username, password
    else:
        return None
    
