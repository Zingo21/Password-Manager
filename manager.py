from cryptography.fernet import Fernet
import getpass
import utils


def main():
    main_password = utils.initialize_main_password()
    key = utils.load_key(main_password)
    cipher = Fernet(key)

    utils.init_db()
    while True:
        print("\nChoose an option:")
        print("1. Generate password")
        print("2. Save password")
        print("3. Get password")
        print("4. Exit")

        choice = input("> ")
        if choice == '1':
            print("Your password:", utils.generate_password())
        elif choice == '2':
            service = input("Service: ")
            username = input("Username: ")
            password = getpass.getpass("Password: ")
            encrypted_password = cipher.encrypt(password.encode('utf-8'))
            utils.save_password(service, username, encrypted_password)
            print("Password has been saved!")
        elif choice == '3':
            service = input("Service: ")
            result = utils.get_password(service, cipher)
            if result:
                username, encrypted_password = result
                print(f"Username: {username}")
                print(f"Password: {password}")
            else:
                print("No passwords has been found.")
        elif choice == '4':
            break
        else:
            print("Invalid selection!")

if __name__ == '__main__':
    main()