from encryption import encrypt_password, decrypt_password
from storage import save_encrypted_password, retrieve_encrypted_password
from auth import authenticate_user, create_user

def main():
    action = input("do you want to create an account or login? (create/login): ").strip().lower()

    if action == "create":
        username = input("enter username: ")
        password = input("enter master password: ")
        
        try:
            # create a new user
            create_user(username, password)
            print("user created successfully.")
        except ValueError:
            print("user already exists. proceeding with authentication...")
            # again prompt for login if account creation fails
            if not authenticate_user(username, password):
                print("authentication failed.")
                return
    elif action == "login":
        username = input("enter username: ")
        password = input("enter master password: ")
        
        if not authenticate_user(username, password):
            print("authentication failed.")
            return
    else:
        print("invalid action.")
        return

    # after successful authentication
    print("authenticated successfully.")
    
    # prompt for next action
    action = input("do you want to save a new password or view an existing one? (save/view): ").strip().lower()

    if action == "save":
        service = input("enter the name of the service: ")
        service_password = input("enter the password for the service: ")
        encrypted_password = encrypt_password(service_password, password)
        save_encrypted_password(username, service, encrypted_password)
        print(f"password for {service} saved successfully.")
    elif action == "view":
        service = input("enter the name of the service to view the password: ")
        encrypted_password = retrieve_encrypted_password(username, service)
        if encrypted_password:
            decrypted_password = decrypt_password(encrypted_password, password)
            print(f"decrypted password for {service}: {decrypted_password}")
        else:
            print(f"no password found for the service '{service}'.")
    else:
        print("invalid action.")

if __name__ == "__main__":
    main()
