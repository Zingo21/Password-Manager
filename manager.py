from cryptography.fernet import Fernet
import getpass
import utils

# Main function
def main():

    # Initialize main password
    main_password = utils.initialize_main_password()

    # Load or create key file
    key = utils.load_key(main_password)
    cipher = Fernet(key)

    # Initialize database
    utils.init_db()
    while True:
        print("\nChoose an option:")
        print("1. Generate password")
        print("2. Save password")
        print("3. Get password")
        print("4. Exit")

        choice = input("> ")

        # If user choose 1, generate a password
        if choice == '1':
            print("Your password:", utils.generate_password())

        # If user choose 2, save a password to the database and encrypt it
        elif choice == '2':
            service = input("Service: ")
            username = input("Username: ")
            password = getpass.getpass("Password: ")
            encrypted_password = cipher.encrypt(password.encode('utf-8'))
            utils.save_password(service, username, encrypted_password)
            print("Password has been saved!")

        # If user choose 3, get a password from the database and decrypt it
        elif choice == '3':
            service = input("Service: ")
            result = utils.get_password(service, cipher)
            if result:
                username, encrypted_password = result
                print(f"Username: {username}")
                print(f"Password: {password}")
            else:
                print("No passwords has been found.")

        # If user choose 4, exit the program
        elif choice == '4':
            break
        else:
            print("Invalid selection!")

if __name__ == '__main__':
    main()