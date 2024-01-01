from datetime import date, timedelta
from models.visit import Visit


class Visitor:
    """Represents a visitor with multiple visits."""

    def __init__(self, visitor_id: str, visits: list[Visit]):
        """
        Initialize Visitor instance.

        Args:
        - visitor_id (str): ID of the visitor.
        - visits (list[Visit], optional): List of Visit instances for the visitor.
        """
        self.visitor_id = visitor_id
        self.visits = visits if visits else []

    def average_time_visit(self) -> timedelta:
        """
        Calculate the average time spent per visit by the visitor.

        Returns:
        - timedelta: Average time spent per visit.
        """
        number_of_valid_visits = 0
        # Retrieve visits with more than one entry
        multi_entry_visits = [visit for visit in self.visits if len(visit.entries) > 1]
        all_entries = [entry for visit in multi_entry_visits for entry in visit.entries]
        if self.visits and len(all_entries) > 1:
            total_duration: timedelta = timedelta()
            for visit in self.visits:
                if len(visit.entries) > 1:
                    duration = visit.duration()
                    total_duration += duration
                    number_of_valid_visits += 1

            return total_duration / number_of_valid_visits
        return timedelta()  # Return zero duration if no visits present

    def daily_visit(self, target_date: date) -> int:
        """
        Get the number of visits made by the visitor on a specific date.

        Args:
        - target_date (date): Date to check for visits.

        Returns:
        - int: Number of visits on the specified date.
        """
        all_entries = [entry for visit in self.visits for entry in visit.entries]
        filtered_entries = [entry for entry in all_entries if entry.date == target_date and entry.delta_time == 0]
        return len(filtered_entries)
