import re

# Function to validate a password based on user-selected criteria
def validate_password(password, criteria):
    # List to store any missing criteria
    missing_criteria = []

    # Check if the length is less than 8, if so, skip further checks
    if len(password) < 8:
        print(f"'{password}' - Invalid password. Less than 8 characters.")
        return

    # Check for uppercase letters (A-Z)
    if '1' in criteria and not re.search(r'[A-Z]', password):
        missing_criteria.append("Uppercase letters")

    # Check for lowercase letters (a-z)
    if '2' in criteria and not re.search(r'[a-z]', password):
        missing_criteria.append("Lowercase letters")

    # Check for numbers (0-9)
    if '3' in criteria and not re.search(r'[0-9]', password):
        missing_criteria.append("Numbers")

    # Check for special characters (!, @, #)
    if '4' in criteria:
        special_characters = re.findall(r'[!@#]', password)
        if len(special_characters) == 0:
            missing_criteria.append("Special characters (!, @, #)")
        elif len(re.findall(r'[^!@#a-zA-Z0-9]', password)) > 0:
            print(f"'{password}' - Invalid password. It contains invalid special characters.")
            return

    # Output results
    if missing_criteria:
        print(f"'{password}' - Invalid password. Missing {', '.join(missing_criteria)}.")
    else:
        print(f"'{password}' - Valid password.")

# Main function
def password_validator():
    # Taking user input for criteria
    criteria = input("Enter the criteria you want to check (1: Uppercase, 2: Lowercase, 3: Numbers, 4: Special characters): ").split()

    # List of passwords to check
    password_list = [
        "Abbbbb@#!",
        "123456789",
        "abcdefg$",
        "abcdefgABHD!@313",
        "abcdefgABHD$$!@313",
    ]

    # Loop through each password and validate
    for password in password_list:
        validate_password(password, criteria)

# Run the validator
password_validator()