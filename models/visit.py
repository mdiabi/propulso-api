from datetime import date, datetime, timedelta

class Entry:
    """Represents an GPS entry sent by a visitor devise."""

    def __init__(self, visitor_id: str, latitude: float, longitude: float, delta_time: int, date: date,
                 time: datetime.time):
        """
        Initialize Entry instance.

        Args:
        - visitor_id (str): ID of the visitor.
        - latitude (float): Latitude coordinate.
        - longitude (float): Longitude coordinate.
        - delta_time (int): Time difference.
            - > 0: Indicates the signal was received before the person was captured in the zone.
            - < 0: Indicates the signal was received after the person was captured in the zone.
            - 0: Indicates the signal was received when the person was in the zone.
        - date (date): Date of the entry.
        - time (datetime.time): Time of the entry.
        """
        self.visitor_id = visitor_id
        self.latitude = latitude
        self.longitude = longitude
        self.delta_time = delta_time
        self.date = date
        self.time = time


class Visit:
    """Represents a visit made by a visitor comprising multiple entries."""

    def __init__(self, entries=None):
        """
        Initialize Visit instance.

        Args:
        - entries (list[Entry], optional): List of Entry instances representing visit entries.
        """
        self.entries = entries if entries else []

    def duration(self) -> timedelta:
        """
        Calculate the duration of the visit.

        Returns:
        - timedelta: Duration of the visit.
        """
        if self.entries:
            start_time = datetime.combine(self.entries[0].date,
                                          datetime.strptime(self.entries[0].time, "%H:%M:%S").time())

            end_time = datetime.combine(self.entries[-1].date,
                                        datetime.strptime(self.entries[-1].time, "%H:%M:%S").time())
            return end_time - start_time
        return timedelta()
