import re

# Part 2: Read passwords from input.txt and validate
def validate_passwords_from_file(filename, criteria):
    valid_count = 0
    invalid_count = 0

    try:
        with open('input.txt', 'r') as file:
            passwords = file.readlines()

        for password in passwords:
            password = password.strip()
            if len(password) < 8:
                print(f"'{password}' - Invalid password. Less than 8 characters.")
                invalid_count += 1
            else:
                missing_criteria = []

                # Check Uppercase letters
                if '1' in criteria and not re.search(r'[A-Z]', password):
                    missing_criteria.append("Uppercase letters")

                # Check Lowercase letters
                if '2' in criteria and not re.search(r'[a-z]', password):
                    missing_criteria.append("Lowercase letters")

                # Check Numbers
                if '3' in criteria and not re.search(r'[0-9]', password):
                    missing_criteria.append("Numbers")

                # Check Special characters
                if '4' in criteria:
                    special_characters = re.findall(r'[!@#]', password)
                    if len(special_characters) == 0:
                        missing_criteria.append("Special characters (!, @, #)")
                    elif len(re.findall(r'[^!@#a-zA-Z0-9]', password)) > 0:
                        print(f"'{password}' - Invalid password. It contains invalid special characters.")
                        invalid_count += 1
                        continue

                # If no missing criteria, the password is valid
                if missing_criteria:
                    print(f"'{password}' - Invalid password. Missing {', '.join(missing_criteria)}.")
                    invalid_count += 1
                else:
                    print(f"'{password}' - Valid password.")
                    valid_count += 1

        # Summary
        print(f"\nTotal valid passwords: {valid_count}")
        print(f"Total invalid passwords: {invalid_count}")

    except FileNotFoundError:
        print(f"The file '{filename}' was not found.")

# Usage
criteria = input("Enter the criteria you want to check (1: Uppercase, 2: Lowercase, 3: Numbers, 4: Special characters): ").split()
validate_passwords_from_file('input.txt', criteria)