from random import choice
import string


class RandomHelper:
    """
    various pseudo randomness

    Returns:
        _type_: static helpers
    """

    @staticmethod
    def remove_from_alphabet(
        alphabet: str,
        exclude: str,
    ) -> str:
        """
        Removes characters from alphabet

        Args:
            alphabet (str): (sic)
            exclude (str): (sic)

        Returns:
            str: cleaned alphabet
        """
        if exclude:
            for letter in exclude:
                alphabet = alphabet.replace(letter, "")
        return alphabet

    @staticmethod
    def random_string(
        length: int = 10,
        alphabet: str = string.ascii_letters + string.digits,
        exclude: str = "oOI ",
    ) -> str:
        """
        Generates a random string, but excludes certain characters for clairity.

        Args:
            length (int, optional): (sic). Defaults to 10.
            alphabet (str, optional): Letter to use. Defaults to string.ascii_letters+string.digits.
            exclude (str, optional): Letters to exclude for clairity.

        Returns:
            str: Random string
        """
        alphabet = RandomHelper.remove_from_alphabet(alphabet, exclude)
        return "".join(choice(alphabet) for _ in range(length))
