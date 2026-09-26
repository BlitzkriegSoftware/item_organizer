class FormatHelper:
    """
    Format helpers

    Returns:
        _type_: Static Methods
    """

    @staticmethod
    def delimiter_every(
        in_text: str, delimiter_every_N: int = 3, delimiter: str = "-"
    ) -> str:
        """
        Delimiter every N characters

        Args:
            in_text (str): (sic)
            delimiter_every_N (int, optional): (sic). Defaults to 3.
            delimiter (str, optional): (sic). Defaults to "-".

        Returns:
            str: delimited string, no hanging delimiters
        """
        if not in_text:
            return ""

        ct: int = 0
        out_text = ""
        for letter in in_text:
            out_text += letter
            ct += 1
            if ct % delimiter_every_N == 0:
                out_text += delimiter

        if out_text.endswith(delimiter):
            out_text = out_text[:-1]

        return out_text
