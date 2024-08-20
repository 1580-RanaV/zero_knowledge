from encryption import encrypt_password, decrypt_password
from storage import save_encrypted_password, retrieve_encrypted_password
from auth import authenticate_user, create_user

def main():
    username = input("Enter username: ")
    password = input("Enter master password: ")
    
    try:
        # Attempt to create a new user
        create_user(username, password)
        print("User created successfully.")
    except ValueError:
        print("User already exists. Proceeding with authentication...")

    # Authenticate user
    if authenticate_user(username, password):
        print("Authenticated successfully.")
        
        # Example option to save or retrieve a password
        action = input("Do you want to save a new password or view an existing one? (save/view): ").strip().lower()

        if action == "save":
            service = input("Enter the name of the service: ")
            service_password = input("Enter the password for the service: ")
            encrypted_password = encrypt_password(service_password, password)
            save_encrypted_password(username, service, encrypted_password)
            print(f"Password for {service} saved successfully.")
        elif action == "view":
            service = input("Enter the name of the service to view the password: ")
            encrypted_password = retrieve_encrypted_password(username, service)
            if encrypted_password:
                decrypted_password = decrypt_password(encrypted_password, password)
                print(f"Decrypted password for {service}: {decrypted_password}")
            else:
                print(f"No password found for the service '{service}'.")
        else:
            print("Invalid action.")
    else:
        print("Authentication failed.")

if __name__ == "__main__":
    main()
