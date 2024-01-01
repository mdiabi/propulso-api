from models.visitors import Visitor

class Store:
    """Represents a store with associated visitors."""

    def __init__(self, store_id: int, visitors: list[Visitor]):
        """
        Initialize Store instance.

        Args:
        - store_id (int): ID of the store.
        - visitors (list[Visitor]): List of Visitor instances associated with the store.
        """
        self.store_id = store_id
        self.visitors = visitors
