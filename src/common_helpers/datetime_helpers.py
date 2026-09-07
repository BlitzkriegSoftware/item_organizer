from datetime import timezone, datetime


class DateTimeHelpers:
    @staticmethod
    def stamp_now_with_z():
        """
        ISO 8601 Timestamp for Now

        Returns:
            ISO 8601 Timestamp
        """
        dt = datetime.now(timezone.utc)
        return DateTimeHelpers.to_iso8601_with_z(dt)

    @staticmethod
    def to_iso8601_with_z(d: datetime):
        """
        Make ISO 8601 Timestamp from DateTime
        With "Z" syntax used for databases and APIs

        Args:
            d (datetime): datetime

        Returns:
            ISO 8601 Timestamp
        """
        if not d:
            raise TypeError("datetime must not be None")

        iso_z = d.isoformat().replace("+00:00", "Z")
        return iso_z

    @staticmethod
    def from_iso8601(iso_string_z: str) -> datetime:
        """
        Converts from ISO 8601 strings
        With or without Z format
        To DateTime

        Args:
            iso_string_z (str): ISO 8601

        Raises:
            TypeError: if empty or None

        Returns:
            datetime: DateTime
        """
        if not iso_string_z:
            raise TypeError("dt None")

        if "z" in iso_string_z.casefold():
            return datetime.fromisoformat(iso_string_z.replace("Z", "+00:00"))
        else:
            return datetime.fromisoformat(iso_string_z)
