import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import platform

# Load secrets from .env file
load_dotenv()

# Function to create schemas in MySQL
def create_schemas(mysql_host, mysql_user, mysql_password, base_name):
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # List of schemas to create
            schemas = [
                base_name,
                f"{base_name}_Timeline",
                f"{base_name}_Hangfire",
                f"{base_name}_IDENTITY"
            ]

            # Create each schema
            for schema in schemas:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{schema}`;")
                print(f"Schema '{schema}' created successfully.")

            # Close cursor
            cursor.close()
    except Error as e:
        print("We can't create the schemas, verify your MySQL credentials.")
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection closed.")

# Masking password for display (showing only first and last characters)
def mask_password(password):
    return f"{mysql_password[0]}{'*' * (len(mysql_password) - 2)}{mysql_password[-1]}" if len(
        mysql_password) > 2 else '*' * len(mysql_password)

# Function to confirm the user's input before proceeding
def confirm_input(mysql_host, mysql_user, mysql_password, base_name):
    print(f"\nPlease confirm your input:")
    print(f"-------------------------------------------")
    print(f"Host: {mysql_host}")
    print(f"User: {mysql_user}")
    print(f"Password: {mask_password(mysql_password)}")
    print(f"Base Name: {base_name}")
    print(f"-------------------------------------------")
    confirmation = input("\nIs this correct? (y/n): ").lower()
    print()
    if confirmation == 'y':
        return True
    else:
        print("Operation canceled.")
        return False

# Function to clear the screen
def clear_screen():
    system = platform.system().lower()
    if system == "windows":
        os.system("cls")
    else:
        os.system("clear")

# Main function
if __name__ == "__main__":
    # MySQL connection details
    mysql_host = input("Enter MySQL host (default: 127.0.0.1): ") or "127.0.0.1"
    mysql_user = input("Enter MySQL user (default: root): ") or "root"
    mysql_password = os.getenv("MYSQL_PASSWORD") or input("MySQL password (default: MYSQL_PASSWORD env var): ")
    if not mysql_password:
        mysql_password = input("Please enter MySQL password: ")
    base_name = input("Enter base name for schemas: ")

    # Confirm the user input
    if confirm_input(mysql_host, mysql_user, mysql_password, base_name):
        # Create schemas if the user confirms
        create_schemas(mysql_host, mysql_user, mysql_password, base_name)

    # Pause execution to keep the window open
    print()
    input("Press any key to exit...")
    clear_screen()
