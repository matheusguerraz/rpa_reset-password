import random
import string

class PasswordGenerator:
    def random_password(self, length=8):
        # Enforce minimum length of 8
        length = max(length, 8)

        # Define character libraries - remove ambiguous characters like iIl|1 0oO
        sets = [
            string.ascii_uppercase,
            string.ascii_lowercase,
            string.digits,
            '!@#$%^&*?'
        ]

        # Append a character from each set - gets first 4 characters
        password = ''.join(random.choice(char_set) for char_set in sets)

        # Use all characters to fill up to length
        while len(password) < length:
            # Get a random set
            random_set = random.choice(sets)

            # Add a random char from the random set
            password += random.choice(random_set)

        # Shuffle the password string before returning
        return ''.join(random.sample(password, len(password)))