from random import choice
import string


class TestHelper:

    @staticmethod
    def random_string(length: int = 10) -> str:
        """Generate a random string of specified length."""
        alphabet = string.ascii_letters + string.digits
        alphabet = alphabet.replace("o", "").replace("I", "")
        return ''.join(choice(alphabet) for _ in range(length))